import os
from google import genai
from dotenv import load_dotenv
import sys

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

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
)
meta = resp.usage_metadata
print(resp.text)
if verbose:
    print(f"User prompt: {prompt}")
    print(f"Prompt tokens: {meta.prompt_token_count}")
    print(f"Response tokens: {meta.candidates_token_count}")
