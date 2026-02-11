import os
import argparse
from dotenv import load_dotenv
from google import genai


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key is None:
    raise RuntimeError("GEMINI_API_KEY non trouvée. Assure-toi d'avoir un fichier .env avec ta clé API.")

client = genai.Client(api_key=api_key)

def main():
    # Now we can access `args.user_prompt`
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt", metavar="user_prompt, ex: uv run main.py 'user_prompt'")
    args = parser.parse_args()
    # Now we can access `args.user_prompt`
    
    
    # gemini-2.5-flash
    generate_content = client.models.generate_content(
        model = 'gemini-2.5-flash',
        contents = args.user_prompt)
    
    if generate_content.usage_metadata is None:
        raise RuntimeError("Failed to retrieve token usage metadata from Gemini response.")
    else:
        print("\nHello from Unibrind-AI-Agent!\n")
        print("Prompt tokens: ", generate_content.usage_metadata.prompt_token_count)
        print("Response tokens: ", generate_content.usage_metadata.candidates_token_count)
        print("\n", generate_content.text)


if __name__ == "__main__":
    main()