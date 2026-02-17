import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
import prompts
import call_function


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key is None:
    raise RuntimeError("GEMINI_API_KEY non trouvée. Assure-toi d'avoir un fichier .env avec ta clé API.")

client = genai.Client(api_key=api_key)

def main():
    # Now we can access `args.user_prompt`
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt", metavar="user_prompt, ex: uv run main.py 'user_prompt'")
    # Now we can access `args.user_prompt`
    
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    
    # gemini-2.5-flash
    generate_content = client.models.generate_content(
        model = 'gemini-2.5-flash',
        contents = messages,
        config=types.GenerateContentConfig(tools=[call_function.available_functions], system_instruction=prompts.system_prompt,temperature=0),
        )
    
    if generate_content.function_calls is not None:
        for items in generate_content.function_calls:
            print(f"Calling function: {items.name}({items.args})")
    else:
        print(generate_content.text)
    
    if generate_content.usage_metadata is None:
        raise RuntimeError("Failed to retrieve token usage metadata from Gemini response.")
    else:
        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {generate_content.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {generate_content.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()