import os
from dotenv import load_dotenv
from google import genai


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key is None:
    raise RuntimeError("GEMINI_API_KEY non trouvée. Assure-toi d'avoir un fichier .env avec ta clé API.")

client = genai.Client(api_key=api_key)

def main():
    print("Hello from Unibrind-AI-Agent!")
    # gemini-2.5-flash
    generate_content = client.models.generate_content(
        model='gemini-2.5-flash',
        contents="Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
    )
    print(generate_content.text)


if __name__ == "__main__":
    main()