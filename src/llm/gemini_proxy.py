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
    interaction = client.interactions.create(
        model="gemini-3.6-flash",
        input=input
    )

    return interaction.output_text

