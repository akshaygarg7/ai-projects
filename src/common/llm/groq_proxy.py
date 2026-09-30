import os

from openai import OpenAI
from langchain_groq import ChatGroq

client = None


def initialize():
    global client
    if client is None:
        client = OpenAI(
            api_key=os.environ.get("GROQ_API_KEY"),
            base_url="https://api.groq.com/openai/v1",
        )


def invoke_model(input):
    initialize()

    payload = input
    if isinstance(payload, str):
        payload = [{"role": "user", "content": payload}]
    elif isinstance(payload, dict):
        payload = [payload]
    elif isinstance(payload, tuple):
        payload = list(payload)

    for message in payload:
        if not isinstance(message, dict):
            raise TypeError("Groq message payload must be a string, dict, or list of dicts.")
        if "role" not in message:
            message["role"] = "user"
        if "content" not in message:
            message["content"] = ""

    response = client.responses.create(
        input=payload,
        model="openai/gpt-oss-120b",
    )
    return response.output_text


def init_langchain_model():
    return ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0,
    )