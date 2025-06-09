import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types


def main():
    if len(sys.argv) <= 1:
        print("Usage: python3 main.py <prompt> [flags]")
        return sys.exit(1)

    user_prompt = sys.argv[1]
    flags = sys.argv[2:]

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)

    generated_content = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
    )

    print(generated_content.text)
    if "--verbose" in flags:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {generated_content.usage_metadata.prompt_token_count}")
        print(
            f"Response tokens: {generated_content.usage_metadata.candidates_token_count}"
        )


if __name__ == "__main__":
    main()
