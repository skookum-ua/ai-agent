import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types


def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("--models", action="store_true", help="Enable available models output")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    
    print("Hello from ai-agent!")

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    
    if api_key == None:
        raise RuntimeError("no api key")
    
    client = genai.Client(api_key=api_key)

    if args.modles == True:
        for model in client.models.list():
            print(f"Model Name: {model.name}")
            print(f"Actions: {model.supported_actions}") 
            #print(f"Input Token Limit: {model.input_token_limit}")
            print("-" * 30)

    try:
        response = client.models.generate_content(model = "gemini-2.5-flash", contents = messages)
    except Exception:
        response = client.models.generate_content(model = "gemini-flash-lite-latest", contents = messages)
    if response.usage_metadata == None:
        raise RuntimeError("no metadata, bad api request")
    
    if args.verbose == True:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    print(f"Response: \n{response.text}")

if __name__ == "__main__":
    main()
