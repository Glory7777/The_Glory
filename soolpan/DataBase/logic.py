import openai
import json
import requests
import os

# OpenAI API 키 설정
openai.api_key = "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"

def get_Liqueur_info(name):
    """Describe the description about a given liqueur name"""
    api_url = "http://127.0.0.1:8000/api/product/"
    api_params = {}

    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Accept-Charset": "utf-8"
    }

    response = requests.get(api_url, params=api_params, headers=headers)
    api_data = response.json()

    for data in api_data:
        if data['name'] == name:
            liqueur_info ={
                "name": name,
                "description": data['dsc']
            }    
            return json.dumps(liqueur_info, ensure_ascii=False)
    else:
        liqueur_info ={
            "name": None,
            "description": None
        }    
        return json.dumps(liqueur_info, ensure_ascii=False)    

def run_conversation(input):
    # Step 1: send the conversation and available functions to GPT

    messages = [{"role": "system", "content": "Only use the functions you have been provided with."},                
        {"role": "user", "content": input}]
    functions = [
        {
            "name": "get_Liqueur_info",
            "description": "Describe in a given name and description.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Product name of the liqueur in a given name.",
                    },
                    "description": {
                        "type": "string",
                        "discription": "description of the liqueur in a given description.",
                    },
                },
                "required": ["name", "description"],                
            },
        }
    ]
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages= messages,
        functions=functions,
        function_call="auto",  # auto is default, but we'll be explicit
    )

    response_message = response["choices"][0]["message"]
  
    # Step 2: check if GPT wanted to call a function
    if response_message.get("function_call"):
        # Step 3: call the function
        # Note: the JSON response may not always be valid; be sure to handle errors
        available_functions = {
            "get_Liqueur_info": get_Liqueur_info,
        }  # only one function in this example, but you can have multiple
        function_name = response_message["function_call"]["name"]

        
        fuction_to_call = available_functions[function_name]
        
        function_args = json.loads(response_message["function_call"]["arguments"])
 

        function_response = fuction_to_call(
            name=function_args.get("name"),            
        )
  

        # Step 4: send the info on the function call and function response to GPT
        messages.append(response_message)  # extend conversation with assistant's reply
        messages.append(
            {
                "role": "function",
                "name": function_name,
                "content": function_response,
            }
        )  # extend conversation with function response
        
        second_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=messages,
        )  # get a new response from GPT where it can see the function response
        assistant_reply = second_response['choices'][0]['message']['content']
        return assistant_reply

