
from openai import OpenAI
from langchain_groq import ChatGroq

import os

client = None

def initialize():
    global client 
    if client == None:
        client = OpenAI(
            api_key=os.environ.get("GROQ_API_KEY"),
            base_url="https://api.groq.com/openai/v1",
        )


def invoke_model(input):
    initialize()

    response = client.responses.create(
        input=input,
        model="openai/gpt-oss-120b",
    )
    # print(response.output_text)

    return response.output_text


def init_langchain_model():
    return ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0,
    )