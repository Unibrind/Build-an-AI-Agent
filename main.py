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
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    
    # Mémoire : Il conserve l'historique (messages). 
    # On initialise ici la liste qui va stocker toute la conversation.
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    
    for _ in range(20):
        generate_content = client.models.generate_content(
            model = 'gemini-2.5-flash',
            contents = messages,
            config=types.GenerateContentConfig(tools=[call_function.available_functions], 
                                            system_instruction=prompts.system_prompt,temperature=0),)
        
        
        # Observation : Il reçoit les instructions du modèle (candidates).
        # On enregistre ce que l'IA vient de répondre ou de demander.
        if generate_content.candidates is not None:
            for x in generate_content.candidates:
                messages.append(x.content)
        
        # On vérifie les métadonnées dès la réception de la réponse
        if generate_content.usage_metadata is None:
            raise RuntimeError("Failed to retrieve token usage metadata from Gemini response.")
        
        # On affiche les tokens à chaque tour si le mode verbose est activé
        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {generate_content.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {generate_content.usage_metadata.candidates_token_count}")
        
        result_from_func = []
        # Action : Il exécute les fonctions si nécessaire.
        if generate_content.function_calls is not None: 
            for items in generate_content.function_calls:
                function_call_result = call_function.call_function(items, verbose=args.verbose)
                
                if function_call_result.parts == []:
                    raise Exception("Empty .parts list")
                
                if function_call_result.parts[0].function_response is None:
                    raise Exception("None FunctionResponse")
                
                if function_call_result.parts[0].function_response.response is None:
                    raise Exception("No function result")
                
                result_from_func.append(function_call_result.parts[0])
                if args.verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
                
            # Réflexion : Il renvoie les résultats à l'IA pour qu'elle décide de la suite.
            # On ajoute les résultats des outils à la mémoire pour le prochain tour de boucle.
            messages.append(types.Content(role="user", parts=result_from_func))
            
        else:
            # Finalisation : Il s'arrête (return) dès qu'il a une réponse textuelle finale.
            print(generate_content.text)
            return


if __name__ == "__main__":
    main()