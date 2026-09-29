# ai-projects
Hands on experience on AI

# from src.proxy.openAiProxy import invoke_model
uv run --env-file .env python -m src.main

uv run --env-file .env python -m src.agents.chat.main
uv run --env-file .env python -m src.agents.web_researcher.research_flow

uv run --env-file .env streamlit run app.py

