
from langchain.agents import create_agent

from src.llm.groq_proxy import init_langchain_model
from src.agents.web_researcher.schema import ResearchState, PlannerOutput, SynthesizeOutput, AnswerOutput
from src.agents.web_researcher.prompts import PROMPT_PLAN, PROMPT_SYNTHESIZE, PROMPT_ANSWER
from src.tools.search import search

# node_function(state, config, runtime) -> state
def planner(state, config, runtime) -> ResearchState:
    print(state.question)
    
    agent = create_agent(
        model=init_langchain_model(),
        system_prompt=PROMPT_PLAN,
        response_format = PlannerOutput,
        debug=False
    )

    input = {"messages": [{"role": "user", "content": state.question}]}

    node_response = agent.invoke(input)

    print(f"sub queries - {node_response["structured_response"].sub_queries}")

    return { "sub_queries": node_response["structured_response"].sub_queries }

def searcher(state, config, runtime) -> ResearchState:

    search_results = search(state.question)

    # print(f"search node - {search_results["results"]}")
    
    node_response = {"search_results": search_results["results"]}
    
    return node_response

def synthesizer(state, config, runtime):
    
    system_prompt = PROMPT_SYNTHESIZE.format(query=state.question, url=state.search_results[0]["url"], scraped_content=state.search_results[0]["content"])

    agent = create_agent(
        model=init_langchain_model(),
        system_prompt=system_prompt,
        response_format = SynthesizeOutput,
    )

    node_response = agent.invoke( {
            "messages": [
                {
                    "role": "user",
                    "content": "Synthesize the provided research content.",
                }
            ]
        })

    # print(node_response["structured_response"])

    return { "findings_formatted": node_response["structured_response"].findings }

def answer(state, config, runtime):

    system_prompt = PROMPT_ANSWER.format(original_query=state.question, findings_formatted_with_numbered_sources=state.findings_formatted)
    agent = create_agent(
        model=init_langchain_model(),
        system_prompt=system_prompt,
        response_format = AnswerOutput,
    )

    node_response = agent.invoke( {
            "messages": [
                {
                    "role": "user",
                    "content": "Generate answer.",
                }
            ]
        })

    strc_res =node_response["structured_response"]
    return { "answer": strc_res.answer , "answer_source": strc_res.source_url }




    # print(f"node state - {state}")
    # print(f"node config - {config}")
    # print(f"node runtime - {runtime}")


        # agent = create_agent(
        # model="",
        # system_prompt=system_prompt,
        # response_format = PlannerOutput,

        # middleware
        # state_schema
        # tools