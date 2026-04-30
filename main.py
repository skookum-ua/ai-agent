import os
import sys
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from functions.get_files_info import schema_get_files_info, get_files_info
from call_functions import available_functions, call_function

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

    if args.models == True:
        for model in client.models.list():
            print(f"Model Name: {model.name}")
            print(f"Actions: {model.supported_actions}") 
            print(f"Input Token Limit: {model.input_token_limit}")
            print("-" * 30)

    for i in range(20):
        try:
            response = call_ai(client, "gemini-2.5-flash", messages )
            #response = client.models.generate_content(model = "gemini-2.5-flash", contents = messages)
        except Exception:
            #response = call_ai(client, "gemini-3-flash-preview", messages )
            response = call_ai(client, "gemini-2.5-flash-lite", messages )
            #response = call_ai(client, "gemini-flash-lite-latest", messages )
            #response = client.models.generate_content(model = "gemini-flash-lite-latest", contents = messages)
        if response.usage_metadata == None:
            raise RuntimeError("no metadata, bad api request")
        
        if response.candidates:
            for i in response.candidates:
                if i.content is not None:
                    messages.append(i.content)

        if args.verbose == True:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        
        list_of_function_results = []
        
        if response.function_calls:
            
            for i in response.function_calls:
                #print(f"Calling function: {i.name}({i.args})")
                function_call_result = call_function(i)
                if not function_call_result.parts:
                    raise Exception(".parts list of function call result is empty")
                if not function_call_result.parts[0].function_response:
                    raise Exception(".function_response is None")
                if not function_call_result.parts[0].function_response.response:
                    raise Exception("actual function result is None")
                
                list_of_function_results.append(function_call_result.parts[0])

                if args.verbose == True:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
        
        else:
            messages.append(types.Content(role="user", parts=list_of_function_results))
        
            print(f"Response: \n{response.text}")

            break
        messages.append(types.Content(role="user", parts=list_of_function_results))
    
    print("maxmum number of iterations reached")
    sys.exit(1)

def call_ai(cli, mod, mess):
    return  cli.models.generate_content(model = mod, contents = mess, config=types.GenerateContentConfig(tools = [available_functions], system_instruction=system_prompt))

if __name__ == "__main__":
    main()
