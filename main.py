import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from schemas import (
    schema_get_files_info,
    schema_get_file_content,
    schema_run_python_file,
    schema_write_file,
)


def main():
    if len(sys.argv) <= 1:
        print("Usage: python3 main.py <prompt> [flags]")
        return sys.exit(1)

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file,
        ]
    )

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
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )

    if len(generated_content.function_calls) > 0:
        calls = []
        for function_call_part in generated_content.function_calls:
            calls.append(
                f"Calling function: {function_call_part.name}({function_call_part.args})"
            )
        print("\n".join(calls))
    else:
        print(generated_content.text)

    if "--verbose" in flags:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {generated_content.usage_metadata.prompt_token_count}")
        print(
            f"Response tokens: {generated_content.usage_metadata.candidates_token_count}"
        )


if __name__ == "__main__":
    main()
