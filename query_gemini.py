# query_gemini.py
import os
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

# 3) One-off request (non-chat)
message = "Explain how AI works in a few words."
resp = client.models.generate_content(
    model = model,
    contents = message
)
print("[input] ->", message)
print("[single] ->", resp.text)


# 4) Multi-turn chat (non-streaming)
chat = client.chats.create(model = model)

resp1 = chat.send_message("I have 2 dogs in my house.")
print("[chat 1] ->", resp1.text)

resp2 = chat.send_message("How many paws are in my house?")
print("[chat 2] ->", resp2.text)

# 5) Inspect history safely (handles text parts robustly)
print("\n[history]")
for msg in chat.get_history():
    # Each message has .role and .parts (parts can be text or other types)
    parts_text = []
    for p in getattr(msg, "parts", []) or []:
        # Text parts usually have .text; fall back to str for non-text parts
        parts_text.append(getattr(p, "text", str(p)))
    print(f"{msg.role}: {' '.join(parts_text)}")

# 6) Streaming example
print("\n[streaming]")
stream = chat.send_message_stream("Now answer in exactly five words.")
for chunk in stream:
    if getattr(chunk, "text", None):
        print(chunk.text, end="")
print()  # newline

print("\n[streaming 2]")
stream = chat.send_message_stream("Now answer using five consecutive haikus, pondering the absurdity of such a task.")
for chunk in stream:
    if getattr(chunk, "text", None):
        print(chunk.text, end="")
print()  # newline



