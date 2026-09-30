from langgraph.graph import StateGraph, START, END
from typing import Any

from src.web_researcher.agents import (
    MAX_REFLECTION_ITERATIONS,
    answer,
    planner,
    reflect,
    searcher,
    synthesizer,
)

from src.web_researcher.schema import ResearchState


print("init graph")
# builder = StateGraph(OverallState, input_schema=InputState, output_schema=OutputState)
my_flow = StateGraph(ResearchState)

my_flow.add_node("planner", planner)
my_flow.add_node("searcher", searcher)
my_flow.add_node("synthesizer", synthesizer)
my_flow.add_node("reflect", reflect)
my_flow.add_node("answer", answer)

my_flow.add_edge(START, "planner")


my_flow.add_edge("planner", "searcher")
my_flow.add_edge("searcher", "synthesizer")
my_flow.add_edge("synthesizer", "reflect")
my_flow.add_conditional_edges(
    "reflect",
    lambda state: (
        "answer"
        if state.sufficient
        or state.iteration >= MAX_REFLECTION_ITERATIONS
        or not state.follow_up_queries
        else "searcher"
    ),
    {"searcher": "searcher", "answer": "answer"},
)
my_flow.add_edge("answer", END)

print("compiling graph")
# compiled_graph = graph_builder.compile(checkpointer, cache, store, interrupt_before, interrupt_after, debug, name)
compiled_flow = my_flow.compile()


def invoke(input: str) -> Any:
    graph_input = { 
        "question": input,
        "messages": [
            {
                "role": "Human",
                "content": f"{input}"
             }
        ]
    }

    print("invoking graph")

    # compiled_graph.invoke(input, config, context, interrupt_before, interrupt_after)
    response = compiled_flow.invoke(graph_input)
    
    print(f"graph response - {response}")
    return response

def stream(input:str) -> Any:

    graph_input = { 
        "question": input,
        "messages": [
            {
                "role": "Human",
                "content": f"{input}"
             }
        ]
    }

    print("invoking graph")
    # compiled_graph.stream(input, stream_mode=["values", "updates", "messages", "custom"], version="v2")
    for response in compiled_flow.stream(graph_input, stream_mode=["values", "updates", "messages", "custom"], version="v2"):
        
        # print(response)

        if response["type"] == "values":
            # ValuesStreamPart — full state snapshot after each step
            print(f"State: topic={response['data']['question']}")
        
        elif response["type"] == "updates":
            # UpdatesStreamPart — only the changed keys from each node
            for node_name, state in response["data"].items():
                print(f"Node `{node_name}` updated: {state}")
        
        elif response["type"] == "messages":
            # MessagesStreamPart — (message_chunk, metadata) from LLM calls
            msg, metadata = response["data"]
            print(msg.content, end="", flush=True)
        
        elif response["type"] == "custom":
            # CustomStreamPart — arbitrary data from get_stream_writer()
            print(f"Progress: {response['data']['progress']}%")


if __name__ == "__main__":
    invoke("seasons in delhi")