import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
import sys
from call_function import available_functions, call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Write or overwrite files
- Execute Python files with optional arguments

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

if len(sys.argv) > 1:
    prompt = sys.argv[1]
else:
    print("Missing prompt.")
    sys.exit(1)

verbose = False
if len(sys.argv) > 2 and sys.argv[2] == "--verbose":
    verbose = True


client = genai.Client(api_key=api_key)

resp = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=prompt,
    config=types.GenerateContentConfig(
        tools=[available_functions], system_instruction=system_prompt
    ),
)

meta = resp.usage_metadata
print(resp.text)
if resp.function_calls:
    for function_call_part in resp.function_calls:
        function_output = call_function(function_call_part, True)
        if function_output.parts[0].function_response.response:
            if verbose:
                print(f"-> {function_output.parts[0].function_response.response}")
                print()
        else:
            raise Exception("Fatal error: invalid tool response")

if verbose:
    print(f"User prompt: {prompt}")
    print(f"Prompt tokens: {meta.prompt_token_count}")
    print(f"Response tokens: {meta.candidates_token_count}")
