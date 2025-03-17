import os
import uuid
from openai import OpenAI
from pyswip import Prolog

client = OpenAI()
client.api_key = os.getenv("OPENAI_API_KEY", "...")

class PrologInterpreterTool:
    def __init__(self):
        self.prolog = Prolog()
        self.pl_file = self._generate_unique_filename()

    def call_openai(self, prompt: str, model: str = "o3-mini", messages: list = None) -> str:
        """
        Calls the OpenAI LLM for advanced summarization or reasoning.
        """
        try:
            if messages is None:
                helper_messages = [{'role': 'user', 'content': prompt}]
            else:
                helper_messages = messages.copy()
                helper_messages.append({'role': 'user', 'content': prompt})

            arguments = {
                "model": model,
                "messages": helper_messages,
            }

            if model.startswith("o1") or model.startswith("o3"):
                arguments["response_format"] = {"type": "text"}
                arguments["reasoning_effort"] = "high"
        
            if model.startswith("gpt"):
                arguments["max_tokens"] = 32000

            response = client.chat.completions.create(**arguments)
            return response.choices[0].message.content
        except Exception as e:
            return f"Error calling LLM model='{model}': {str(e)}"

    def _generate_unique_filename(self):
        """
        Generates a unique filename using a GUID and ensures that no file with that name exists.
        """
        while True:
            filename = f"{uuid.uuid4()}.pl"
            if not os.path.exists(filename):
                return filename

    def convert_nl_rules_to_prolog(self, rules_text):
        """
        Dynamically converts a natural language set of rules into Prolog code.
        Uses the OpenAI API with the "o3-mini" model to create equivalent Prolog predicates.
        The prompt instructs the model to translate the rules, and the returned code is cleaned and returned.
        """
        prompt = (
            "You are an expert in Prolog logic programming. Given the following business rules, "
            "generate equivalent Prolog code. "
            "Always use a check_valid predicate to return True or False instead of prolog default behavior of pass or fail for validations.\n\n"
            "% check_valid(+Goal, -Result) check_valid(Goal, 'True') :- call(Goal), !. check_valid(_Goal, 'False').\n\n"
            "The rules are:\n\n"
            f"{rules_text}\n\n"
            "Output only valid Prolog code (do not include markdown formatting)."
        )
        
        try:
            prolog_code = self.call_openai(prompt)
            # Clean up any markdown triple-backticks if present.
            filtered_lines = [line for line in prolog_code.splitlines() if not line.strip().startswith("```")]
            prolog_code = "\n".join(filtered_lines).strip()
            return prolog_code
        except Exception as e:
            print("Error during conversion via OpenAI API:", e)
            raise

    def load_rules(self, rules_text):
        """
        Converts the natural language rules into Prolog code using dynamic OpenAI conversion,
        writes the code to a uniquely named file, and consults it using the Prolog engine.
        """
        print("\n[INFO] Generating Prolog code from provided rules...")
        prolog_code = self.convert_nl_rules_to_prolog(rules_text)
        #print("\n[INFO] Generated Prolog code:\n", prolog_code)
        with open(self.pl_file, "w") as f:
            f.write(prolog_code)
        print(f"\n[INFO] Consulting generated Prolog file: {self.pl_file}")
        self.prolog.consult(self.pl_file)

    def convert_english_query_to_prolog(self, english_query: str) -> str:
        """
        Converts an English description of a test case to a valid Prolog query.
        It reads the generated Prolog rules to provide context to the LLM.
        """
        try:
            with open(self.pl_file, "r") as f:
                prolog_code = f.read()
        except Exception as e:
            print("Error reading Prolog code file:", e)
            raise

        # Create a prompt that shows the context (the Prolog predicates) and then asks for a query.
        prompt = (
            "You are an expert in Prolog and you have been given a dynamically generated Prolog program "
            "designed to encode the following business rules:\n\n"
            f"{prolog_code}\n\n"
            "Based on this logic, convert the following English test case description into a valid Prolog query suitable to be called with pyswip’s query function (which means it should never start with ?- and be without explanations or extra commentary). Response code must bind any computed results to variables so that they can be extracted upon query execution. Output only the Prolog query without any markdown formatting.\n\n"
            f"English description: {english_query}"
        )
        
        prolog_query = self.call_openai(prompt)
        # Clean up any markdown formatting if present.
        filtered_lines = [line for line in prolog_query.splitlines() if not line.strip().startswith("```")]
        prolog_query = "\n".join(filtered_lines).strip()
        return prolog_query

    def query(self, query_text):
        """
        Executes a Prolog query (provided as a string without the ending period)
        and returns a list of solutions found.
        """
        try:
            results = list(self.prolog.query(query_text))
            return results
        except Exception as e:
            print("Error executing query:", e)
            return []

    def get_english_answer(self, query, prolog_query, prolog_results):
        prompt = f"Given this english query, and associated prolog interpretation along with prolog answer. Give an english answer to the question based on the prolog results without mentioning any system internals on how the answer was derived using prolog.\n\nEnglish query:\n{query}\n\nProlog Query:\n{prolog_query}\n\nProlog Results:\n{prolog_results}"
        return self.call_openai(prompt)

    def clean_up(self):
        os.remove(self.pl_file)

    def print_answer(self,query):
        print("\n[QUESTION]:", query)
        prolog_query = self.convert_english_query_to_prolog(query)
        print("\n[INFO] Executing Prolog query:", prolog_query)
        prolog_results = self.query(prolog_query)
        print("\n[INFO] Prolog results:", prolog_results)
        answer = self.get_english_answer(query, prolog_query, prolog_results)
        print("\n[FINAL ANSWER] ")
        print(answer)

def main():

    # https://explorer.invariantlabs.ai/u/invariant/tau-bench_claude-3-5-sonnet/t/923
    sample_rules_text = """
    - Passengers: Each reservation can have at most five passengers. The agent needs to collect the first name, last name, and date of birth for each passenger. All passengers must fly the same flights in the same cabin.
    - Payment: each reservation can use at most one travel certificate, at most one credit card, and at most three gift cards. The remaining amount of a travel certificate is not refundable. All payment methods must already be in user profile for safety reasons.
    - Checked bag allowance: If the booking user is a regular member, 0 free checked bag for each basic economy passenger, 1 free checked bag for each economy passenger, and 2 free checked bags for each business passenger. If the booking user is a silver member, 1 free checked bag for each basic economy passenger, 2 free checked bag for each economy passenger, and 3 free checked bags for each business passenger. If the booking user is a gold member, 2 free checked bag for each basic economy passenger, 3 free checked bag for each economy passenger, and 3 free checked bags for each business passenger. Each extra baggage is 50 dollars."""

    tool = PrologInterpreterTool()
    tool.load_rules(sample_rules_text)

    print("" * 80)
    print("TEST CASES")
    print("" * 80)
    print("Example 1:")
    query = (
    "Verify that a reservation with the following three passengers: "
    "John Doe (born 1990-01-01), Jane Doe (born 1991-02-02), and Alice Smith (born 1992-03-03) "
    "satisfies the rule that a reservation can include at most five passengers with complete first name, "
    "last name, and date of birth information, and that they are on the same flights and cabin. "
    "Return the query to check for valid passengers."
    )
    tool.print_answer(query)

    print("*" * 80)
    print("Example 2:")
    query = (
    "Check that a reservation that uses 0 travel certificates, 1 credit card, and 2 gift cards "
    "is valid according to the payment rules."
    )
    tool.print_answer(query)

    print("*" * 80)
    print("Example 3:")
    query = (
    "Determine the baggage fee for a silver member traveling as an economy passenger who has booked 4 checked bags "
    "according to the baggage rules."
    )
    tool.print_answer(query)

    print("*" * 80)
    print("Example 4:")
    query = (
    "Verify that a reservation with the following three passengers: "
    "Alice Johnson (born 1985-07-07), Bob Smith (born 1986-08-08), and Carol Danvers (born 1987-09-09) "
    "who are all booked on flight AA101 in Economy cabin, uses 0 travel certificates, 1 credit card, and 3 gift cards "
    "and that for a silver member traveling in Economy, booking total of 5 checked bags, "
    "Return the combined query to check for valid passengers, valid payment, and the proper baggage fee."
    )
    tool.print_answer(query)

    print("*" * 80)
    print("Example 5:")
    query = (
    "Check that a reservation with the following six passengers: "
    "   1) John Doe (born 1990-01-01), "
    "   2) Jane Doe (born 1991-02-02), "
    "   3) Alice Smith (born 1992-03-03), "
    "   4) Bob Brown (born 1993-04-04), "
    "   5) Carol White (born 1994-05-05), "
    "   6) David Black (missing date of birth), "
    "all booked on flight AA202 in Business cabin, uses 2 travel certificates, 1 credit card, and 4 gift cards, "
    "and that for a regular member traveling in Business, booking total of 6 checked bags, "
    "Return the combined query to check for valid passengers, valid payment, and the proper baggage fee."
    )
    tool.print_answer(query)

    tool.clean_up()

if __name__ == "__main__":
    main()
