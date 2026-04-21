import argparse
import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from functions.call_function import available_functions, call_function



def main():
    parser = argparse.ArgumentParser(description="AI Code Assistant")
    parser.add_argument("user_prompt", type=str, help="Prompt to send to Gemini")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()


    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")

    client = genai.Client(api_key=api_key)
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    for _ in range(20):
        final_text = generate_content(client, messages, args.verbose)
        if final_text:
            print("Final response:")
            print(final_text)
            return final_text

    print("Maximum iterations reached")
    sys.exit(1)



def generate_content(client, messages,verbose):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
    )
    if not response.usage_metadata:
        raise RuntimeError("Gemini API response appears to be malformed")

    if verbose:
        print(f"User prompt: {messages}")
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    functions = []

    if response.candidates:
        for candidate in response.candidates:
            if candidate.content:
                messages.append(candidate.content)

    if not response.function_calls:
        return response.text

    for function_call in response.function_calls:
        function_call_result = call_function(function_call,verbose)
        if (
        not function_call_result.parts 
        or not function_call_result.parts[0].function_response 
        or not function_call_result.parts[0].function_response.response
        ):
            raise RuntimeError("empty function response")
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
            print("Response:")
            
        functions.append(function_call_result.parts[0])


        print(f"Calling function: {function_call.name}({function_call.args},)")


    messages.append(types.Content(role="user", parts=functions))

    

if __name__ == "__main__":
    main()
