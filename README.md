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
 
