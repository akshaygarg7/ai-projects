import os

from google import genai

client = None

def init():
    global client
    if client == None:
        client = genai.Client(
            api_key=os.environ.get("GEMINI_API_KEY"),
        )

def invoke_model(input):
    init()

    if isinstance(input, list):
        prompt = "\n".join(
            f"{message['role']}: {message['content']}" for message in input
        )
    else:
        prompt = input

    interaction = client.interactions.create(
        model="gemini-3.6-flash",
        input=prompt
    )

    return interaction.output_text

