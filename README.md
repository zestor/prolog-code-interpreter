# Prolog Interpreter Tool with OpenAI-Assisted Rule Conversion

## Overview
This project leverages natural language processing and logic programming by dynamically converting human-readable business rules into Prolog code. It then uses the Prolog engine (via pyswip) to validate and query these rules. The conversion process is powered by the OpenAI large language models (LLMs), which translate natural language descriptions both for generating appropriate Prolog predicates and for formulating queries based on test case descriptions.

## Features
• Dynamic conversion of natural language business rules into valid Prolog predicates.
• Automatic file management using uniquely generated Prolog filenames.
• Use of a “check_valid” predicate to enforce strict validation behavior in Prolog queries.
• Conversion of English test case descriptions into executable Prolog queries.
• Execution of Prolog queries with result handling and error reporting.
• Integration with OpenAI’s chat completion API for advanced summarization and rule translation.

## Project Structure
main.py        - Main entry point of the application containing the PrologInterpreterTool class and demonstration examples.
README.md      - This file with comprehensive project documentation.

## Dependencies
• Python 3.7+
• openai (Python package) – For LLM interactions with OpenAI’s API.
• pyswip – Python interface to SWI-Prolog.

To install the required Python libraries, run:

pip install openai pyswip

## Configuration
Before running this project, ensure you have set up your OpenAI API key. The API key can be set as an environment variable:

For Unix/Linux/MacOS:

export OPENAI_API_KEY="your-openai-api-key"
For Windows (Command Prompt):

set OPENAI_API_KEY="your-openai-api-key"
Alternatively, you can replace the default placeholder ("...") in the code with your API key, though using environment variables is more secure.

## Usage
Prepare the environment by installing the required packages and setting up your OpenAI API key.

Run the main.py script:

 python main.py
 
The script provides several examples demonstrating:

Loading a set of natural language business rules.
Converting these rules into Prolog code using the OpenAI model.
Saving and consulting the Prolog code with pyswip.
Converting various English descriptions of test cases into valid Prolog queries.
Executing these queries against the Prolog engine and displaying results.
Each segment of the output shows:

The English description being tested.
The generated Prolog query.
The results of executing the query.
How It Works
PrologInterpreterTool Class:

_generate_unique_filename:
Generates a globally unique .pl (Prolog) file name ensuring no conflicts.

call_openai:
This method sends prompts to the OpenAI chat model specified (defaults to "o3-mini") to receive advanced natural language processing outputs. Special parameters like "response_format" and "max_tokens" are adjusted based on the model in use.

convert_nl_rules_to_prolog:
Receives raw business rules in English and constructs a prompt for the LLM to produce Prolog predicates. The response is cleaned of any markdown formatting before use.

load_rules:
Writes the generated Prolog code into a uniquely named file and uses the pyswip Prolog interpreter to consult (load) the code.

convert_english_query_to_prolog:
Reads the active Prolog code (context), then sends an English test case to OpenAI to obtain a valid Prolog query. The generated query is prepared for direct execution with pyswip.

query:
Executes a provided Prolog query using pyswip and returns a list of solutions or handles errors during execution.

main Function:

Demonstrates the complete flow by:
Converting a static set of business rules related to a reservations and travel system (passenger limits, payment restrictions, checked bag allowances) into Prolog.
Executing a series of example queries (both positive and negative scenarios) which check various aspects of reservation validity.
Extending the Project
• Update Business Rules:
Modify the 'sample_rules_text' string in main.py to reflect different or additional business rules. The framework will automatically convert these rules to Prolog code.

• Custom Queries:
Use the tool's convert_english_query_to_prolog method to generate Prolog queries from new English descriptions. This facilitates rapid testing and validation of the defined business logic.

• Model Parameters:
The call_openai function handles different model types (e.g., GPT-based or "o3"/"o1" variants). You can adjust the model or add additional parameters as necessary.

Troubleshooting
• OpenAI API Errors:
If the LLM fails to process a prompt or returns an error, confirm that your API key is correctly set and that you have internet connectivity.

• pyswip Issues:
Ensure that SWI-Prolog is installed and properly set up on your system, as pyswip serves as an interface to it. Visit https://www.swi-prolog.org for installation details.

• File Permissions:
The script writes generated Prolog code to disk. Ensure that the script has write permissions to the current directory.
