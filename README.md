# Prolog Interpreter Tool with OpenAI-Assisted Rule Conversion

## Overview
This project leverages natural language processing and logic programming by dynamically converting human-readable business rules into Prolog code. It then uses the Prolog engine (via pyswip) to validate and query these rules. The conversion process is powered by the OpenAI large language models (LLMs), which translate natural language descriptions both for generating appropriate Prolog predicates and for formulating queries based on test case descriptions.

## Features
- Dynamic conversion of natural language business rules into valid Prolog predicates.
- Automatic file management using uniquely generated Prolog filenames.
- Use of a “check_valid” predicate to enforce strict validation behavior in Prolog queries.
- Conversion of English test case descriptions into executable Prolog queries.
- Execution of Prolog queries with result handling and error reporting.
- Integration with OpenAI’s chat completion API for advanced summarization and rule translation.

## Project Structure
- main.py        Main entry point of the application containing the PrologInterpreterTool class and demonstration examples.
- README.md      This file with comprehensive project documentation.

## Dependencies
- Python 3.7+
- openai (Python package) – For LLM interactions with OpenAI’s API.
- pyswip – Python interface to SWI-Prolog.

To install the required Python libraries, run:
```
pip install openai pyswip
```
## Configuration
Before running this project, ensure you have set up your OpenAI API key. The API key can be set as an environment variable:

For Unix/Linux/MacOS:
```
export OPENAI_API_KEY="your-openai-api-key"
```
For Windows (Command Prompt):
```
set OPENAI_API_KEY="your-openai-api-key"
```
Alternatively, you can replace the default placeholder ("...") in the code with your API key, though using environment variables is more secure.

## Usage
Prepare the environment by installing the required packages and setting up your OpenAI API key.

Run the main.py script:
```
 python main.py
```



## Prolog Installation Instructions
Below are extra installation instructions for setting up SWI-Prolog on different operating systems to work with pyswip:

### MacOS:

- Install Homebrew if you haven’t already. Open the Terminal and run:
```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
- Use Homebrew to install SWI-Prolog:
```
brew install swi-prolog
```
- Verify the installation by running:
```
swipl --version
```

### Linux (Debian/Ubuntu-based):

- Update your package lists:
```
sudo apt-get update
```
- Install SWI-Prolog:
```
sudo apt-get install swi-prolog
```
- Verify the installation:
```
swipl --version
```

### Fedora: 
```
sudo dnf install swi-prolog
```

### CentOS/RedHat: 
```
sudo yum install swi-prolog 
```
Note: If not available via yum/dnf, refer to your distro’s repository or build from source.

### Windows:

- Visit the official SWI-Prolog download page: https://www.swi-prolog.org/Download.html
- Download the Windows Installer (".exe" file) for the latest version.
- Run the installer and follow the setup instructions.
- Once installed, add the SWI-Prolog “bin” directory to your system’s PATH if the installer hasn’t done so automatically. This ensures that pyswip can locate the SWI-Prolog executable.
- To modify the PATH environment variable, search for “Environment Variables” in the Windows start menu, then under System Properties, click on “Environment Variables...” and edit the “Path” variable to include the path to SWI-Prolog (e.g., C:\Program Files\swipl\bin).
- Verify the installation by opening Command Prompt and running:
```
swipl --version
```

## After Installing SWI-Prolog

- Ensure you can run SWI-Prolog from your command line (Terminal, Command Prompt, etc.) using the command "swipl".
- pyswip will rely on the SWI-Prolog executable being available in your PATH. If you encounter issues with pyswip not finding Prolog, double-check your PATH settings.
- Once SWI-Prolog is installed correctly, you can use pyswip in your Python projects to consult and query Prolog code seamlessly.
- These detailed steps should help ensure that SWI-Prolog is installed on your system, allowing pyswip to function correctly within this project.
