import openai
import json
import requests
import os
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
import Levenshtein
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

# OpenAI API 키 설정
openai.api_key = os.getenv('API_KEY')

global_api_url = None #전역변수 지정

def return_api_url(api_url):
    global global_api_url  # 전역 변수 사용 선언
    global_api_url = api_url #전역 변수 할당
    return global_api_url #전역 변수로 api 리턴

def get_Liqueur_info(name):

    """Describe the description about a given liqueur name"""
    
    api_url = return_api_url(global_api_url) #전역변수 입력 후 api데이터 호출(정상적동 확인완료)
    api_params = {}

    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Accept-Charset": "utf-8"
    }

    response = requests.get(api_url, params=api_params, headers=headers)
    api_data = response.json()
    threshold = 1
    for data in api_data:     
        if Levenshtein.distance(data['name'], name) <= threshold:
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
    try:
    
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
            if assistant_reply == "":
                assistant_reply = "요청하신 정보를 찾을 수 없습니다. 다른 질문을 해주세요!"
            
            return assistant_reply
    
    except:
        assistant_reply = "요청하신 정보를 찾을 수 없습니다. 다른 질문을 해주세요!"
