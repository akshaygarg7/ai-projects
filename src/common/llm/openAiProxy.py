from openai import OpenAI
import os

MODEL = "gpt-5.6-luna"

client = OpenAI()

def invoke_model(input):
    try:
        print("calling model")
        response = client.responses.create(
            model="gpt-5.6-luna",
            input=input,
        )

        print(response.output_text)

        return response.output_text
    except Exception as e:
        print(f"falied - {e}")