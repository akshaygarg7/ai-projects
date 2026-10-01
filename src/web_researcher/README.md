## Web Researcher Design

The web-researcher is a LangGraph stateful workflow. Its shared state carries the question, search results, accumulated findings, reflection results, and final answer.

The workflow runs these steps:

1. **Planner** proposes focused search subqueries.
2. **Searcher** searches Tavily. The initial search currently uses the original question; follow-up rounds use queries proposed by reflection.
3. **Synthesizer** extracts findings with source URLs. It currently synthesizes the first result in each search batch, retaining findings from earlier rounds.
4. **Reflector** evaluates whether the findings answer the question, identifies gaps or contradictions, and proposes follow-up queries when useful.
5. **Answerer** writes the final response from the collected findings, with source citations.

Reflection can route the workflow back to search. It stops when the findings are sufficient, there are no follow-up queries, or the two-search-round limit is reached.

## Calling the Workflow

Both functions accept a question string and run the compiled LangGraph workflow with that question in its state.

### `invoke(question)`

`invoke` runs the workflow synchronously with `compiled_flow.invoke()`. It waits for the full research run, prints the final answer and selected source URL, and returns only the answer text:

```python
from src.web_researcher.research_flow import invoke

answer = invoke("What are the latest developments in battery recycling?")
print(answer)
```

### `stream(question, on_progress=None)`

`stream` is an iterator backed by `compiled_flow.stream(..., stream_mode="updates")`. As graph nodes finish, it calls the optional `on_progress` callback with labels such as `Searching the web` and `Synthesizing findings`. When the answer node finishes, it yields the completed answer with its source URL:

```python
from src.web_researcher.research_flow import stream

for text in stream("What are the latest developments in battery recycling?", on_progress=print):
	print(text, end="")
```

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


