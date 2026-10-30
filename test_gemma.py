from config import GEMINI_API_KEY, GEMMA_MODEL
from google import genai
from google.genai import types

# 1. Catch missing .env variables early
if not GEMINI_API_KEY:
    print("ERROR: API Key not loaded! Check your .env file.")
    exit(1)

# 2. Add an explicit timeout (e.g., 30 seconds)
client = genai.Client(
    api_key=GEMINI_API_KEY,
    http_options=types.HttpOptions(timeout=30000) 
)

# 3. Swap GEMMA_MODEL for "gemini-2.5-flash" if it still times out
TEST_MODEL = GEMMA_MODEL 

print(f"Sending request to {TEST_MODEL}...")

try:
    response = client.models.generate_content(
        model=TEST_MODEL,
        contents="Say hello in Swahili, in one sentence.",
    )
    print("\nSuccess:")
    print(response.text)
except Exception as e:
    print("\nRequest failed:")
    print(e)