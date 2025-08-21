# Gemini API in Python Walkthrough

This guide provides instructions on setting up your environment and using the Gemini API with Python in VSCode.

## Setting up the Repository

You can set up your project either from scratch or by using a pre-configured template.

### From Scratch

1.  **Create a New Repository:** Use GitHub and GitHub Desktop to create a new repository.
2.  **Open in GitHub Desktop:**
    - Navigate to your new repository on GitHub.
    - Click `Code` and then `Open with GitHub Desktop`.
3.  **Clone and Open in VSCode:** In GitHub Desktop, clone the repository to your local machine and then open it in VSCode (e.g., via `Repository > Open in Visual Studio Code`).
4.  **Set up Virtual Environment:**
    - In VSCode, open a new terminal (`Terminal > New Terminal`).
    - Run the following commands:
      ```bash
      python -m venv .venv
      .venv/Scripts/activate
      ```
    - Verify your terminal has a green `(.venv)` on the left.
5.  **Select Python Interpreter:**
    - Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac).
    - Type and select `Python: Select Interpreter`.
    - Choose `Python x.xx.x (.venv)`.
6.  **Create `.env` file:**
    - Create a file named `.env` in the root of your project (ensure it's **not** inside the `.venv` folder).
    - Ensure your `.gitignore` file includes `.env` and `.venv`. (This is often pre-configured if you use a Python `.gitignore` template).
    - Inside `.env`, add a placeholder: `GEMINI_API_KEY = 'enter_key_here'`
7.  **Install Dependencies:**
    - In your activated virtual environment terminal, run:
      ```bash
      pip install python-dotenv google-genai google-generativeai
      ```
      _(Note: `google-generativeai` is an older library sometimes used in tutorials; `google-genai` is the current recommendation)._
8.  **Save Dependencies to `requirements.txt`:**
    - Run: `pip freeze > requirements.txt`
    - _(To install packages from this file later, you would run `pip install -r requirements.txt`)_
9.  **Push to GitHub:**
    - In your terminal, commit and push your changes:
      ```bash
      git add .
      git commit -m "Initialise repo"
      git push origin main
      ```
    - Verify on GitHub that your `requirements.txt` (and `.gitignore` if created) are added.

### From Template (Quick Start)

1.  **Fork the Template Repository:**
    - Visit [https://github.com/Jaffulee/gemini_api_template](https://github.com/Jaffulee/gemini_api_template).
    - Click `Fork` at the top right to create your own copy of the repository.
    - Name your repository as desired.
2.  **Open in GitHub Desktop:**
    - Navigate to your forked repository on GitHub.
    - Click `Code` and then `Open with GitHub Desktop`.
3.  **Clone and Open in VSCode:** In GitHub Desktop, clone the repository and open it in VSCode (e.g., via `Repository > Open in Visual Studio Code`).
4.  **Set up Virtual Environment:**
    - In VSCode, open a new terminal (`Terminal > New Terminal`).
    - Run the following commands:
      ```bash
      python -m venv .venv
      .venv/Scripts/activate
      ```
    - Verify your terminal has a green `(.venv)` on the left.
5.  **Select Python Interpreter:**
    - Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac).
    - Type and select `Python: Select Interpreter`.
    - Choose `Python x.xx.x (.venv)`.
6.  **Install Dependencies:**
    - In your activated virtual environment terminal, run:
      ```bash
      pip install -r requirements.txt
      ```
7.  **Create `.env` file:**
    - Create a file named `.env` in the root of your project (ensure it's **not** inside the `.venv` folder).
    - Inside `.env`, add a placeholder: `GEMINI_API_KEY = 'enter_key_here'`

## API Keys and Environment Variables

Before querying Gemini, you'll need an API key.

- **Gemini API Pricing:** The free tier is generally sufficient for experimentation.
  - [https://ai.google.dev/gemini-api/docs/pricing](https://ai.google.dev/gemini-api/docs/pricing)
- **Gemini API Documentation:**
  - [https://ai.google.dev/gemini-api/](https://ai.google.dev/gemini-api/)
  - This example is based on the text generation section: [https://ai.google.dev/gemini-api/docs/text-generation?\_gl=1*u7njbu*\_up*MQ..*\_ga*MTM0Njg5NTg4MC4xNzU1Nzg2OTU1*\_ga_P1DBVKWT6V\*czE3NTU3ODY5NTQkbzEkZzAkdDE3NTU3ODY5NTQkajYwJGwwJGgxOTQ3Nzc1ODI5#python_2](https://ai.google.dev/gemini-api/docs/text-generation?_gl=1*u7njbu*_up*MQ..*_ga*MTM0Njg5NTg4MC4xNzU1Nzg2OTU1*_ga_P1DBVKWT6V*czE3NTU3ODY5NTQkbzEkZzAkdDE3NTU3ODY5NTQkajYwJGwwJGgxOTQ3Nzc1ODI5#python_2)

**To obtain your API Key:**

1.  Using your Google account, visit: [https://aistudio.google.com/apikey](https://aistudio.google.com/apikey)
2.  Click `+ Create API key`.
3.  Copy your new API key.
4.  Paste this key into your `.env` file, replacing the placeholder: `GEMINI_API_KEY = 'YOUR_ACTUAL_API_KEY_HERE'`

## Querying Gemini through Python

1.  **Create Python File:**
    - Create a new Python file (e.g., `query_gemini.py`) in the root of your project (ensure it's **not** inside the `.venv` folder).
2.  **Add Code:**

    - In `query_gemini.py`, add the following Python code. This code demonstrates:
      - Importing necessary packages.
      - Loading your API key from `.env`.
      - Initializing the Gemini client.
      - Performing a one-off text generation request.
      - Conducting a multi-turn chat.
      - Inspecting chat history.
      - Streaming responses.

    ```python
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
    ```

3.  **Run the Script:** - Save the `query_gemini.py` file. - In your VSCode terminal (with the virtual environment activated), run:
    `bash
python query_gemini.py
`
    The output will be printed directly in your console.

4.  **Push to GitHub:**
    - In your terminal, commit and push your changes:
      ```bash
      git add .
      git commit -m "Message_here"
      git push origin main
      ```
