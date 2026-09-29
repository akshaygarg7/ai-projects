from src.llm.groq_proxy import invoke_model as groq
from src.llm.gemini_proxy import invoke_model as gemini


def invoke(input):

    try:
        model_response = groq(input)
        # model_response = gemini(input)
        return model_response
    except Exception as e:
        print(e)


if __name__ == "__main__":
    invoke("hello")