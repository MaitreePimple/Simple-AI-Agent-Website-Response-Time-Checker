import os
import google.generativeai as genai
from dotenv import load_dotenv
from action import get_response_time
from prompt import system_prompt
from json_helpers import extract_json

load_dotenv()

# Configure Gemini with your API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_text_with_conversation(messages, model="gemini-1.5-flash", temperature=0.7, max_tokens=150):
    try:
        # Join messages into a single conversation text
        conversation_text = "\n".join([f"{m['role'].upper()}: {m['content']}" for m in messages])

        # Create model
        model = genai.GenerativeModel(model)
        response = model.generate_content(
            conversation_text,
            generation_config=genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens,
            )
        )
        return response.text
    except Exception as e:
        print(f"⚠️ Gemini API Error: {e}")
        return None

available_actions = {
    "get_response_time": get_response_time
}

user_prompt = "What is the response time for google.com?"

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": user_prompt}
]

turn_count = 1
max_turns = 5

while turn_count < max_turns:
    print(f"Loop :{turn_count}")
    print("------------------------------------")
    turn_count += 1

    response = generate_text_with_conversation(messages)

    if not response:
        break

    print(response)

    json_function = extract_json(response)

    if json_function:
        function_name = json_function[0]['function_name']
        function_parms = json_function[0]['function_parms']
        if function_name not in available_actions:
            raise Exception(f"Unknown action: {function_name}:{function_parms}")
        print(f"--running {function_name} {function_parms}")
        action_function = available_actions[function_name]

        result = action_function(**function_parms)
        function_result_message = f"Action_Response: {result}"
        messages.append({"role": "user", "content": function_result_message})
        print(function_result_message)
    else:
        break
