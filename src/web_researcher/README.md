## Web Researcher Design

The web-researcher is a LangGraph stateful workflow. Its shared state carries the question, search results, accumulated findings, reflection results, and final answer.

The workflow runs these steps:

1. **Planner** proposes focused search subqueries.
2. **Searcher** searches Tavily. The initial search currently uses the original question; follow-up rounds use queries proposed by reflection.
3. **Synthesizer** extracts findings with source URLs. It currently synthesizes the first result in each search batch, retaining findings from earlier rounds.
4. **Reflector** evaluates whether the findings answer the question, identifies gaps or contradictions, and proposes follow-up queries when useful.
5. **Answerer** writes the final response from the collected findings, with source citations.

Reflection can route the workflow back to search. It stops when the findings are sufficient, there are no follow-up queries, or the two-search-round limit is reached.

## Run the Web Researcher

Requirements: Python 3.14 or later, [uv](https://docs.astral.sh/uv/), and API keys for Groq and Tavily.

Install the project dependencies:

```sh
uv sync
```

Create a `.env` file in the repository root with your keys:

```dotenv
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

Run the web-researcher module with its built-in example question:

```sh
uv run --env-file .env python -m src.web_researcher.research_flow
```

To ask a custom question from the command line:

```sh
uv run --env-file .env python -c 'from src.web_researcher.research_flow import invoke; invoke("What are the latest developments in battery recycling?")'
```


