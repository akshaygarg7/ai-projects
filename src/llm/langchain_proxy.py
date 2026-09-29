import os

from langchain.agents import create_agent

client = None

def init():
    global client
    if client == None:
        client = genai.Client(
            api_key=os.environ.get("GEMINI_API_KEY"),
        )

def create_agent(system_prompt):
    init()
    agent = create_agent(
        model="gpt-5.6-luna",
        system_prompt=system_prompt
        response_format

        # middleware
        # state_schema
        # tools
    )