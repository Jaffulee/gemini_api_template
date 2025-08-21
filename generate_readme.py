import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai

# Save model version used as a string
model = "gemini-2.5-flash"

# 1) Load API key from .env (GEMINI_API_KEY=your_key with no quotes)
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY not set. Check your .env file.")

# 2) Init client
client = genai.Client(api_key=api_key)

# 3) Get input information from text file
input_path = Path('Inputs','draft_instructions.txt')

try:
    message_data = input_path.read_text(encoding="utf-8")
except UnicodeDecodeError:
    # Handles files saved with a BOM from some editors
    message_data = input_path.read_text(encoding="utf-8-sig")

# 4) One-off request (non-chat)
message_base = "I want to create a README.md for my instructions about how to get set up with using Gemini in VSCode via Python. I have written some draft instructions, but want it to be formatted as a README. Here are the full draft instructions. Only respond with the markdown and nothing else.\n"

message = message_base + message_data

resp = client.models.generate_content(
    model = model,
    contents = message
)
text = resp.text
print(text)

# 5) Write to the file README_GENERATED.md
output_path = Path("README_GENERATED.md")
output_path.write_text(text, encoding="utf-8")
print(f"Wrote {output_path}")
