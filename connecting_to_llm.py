from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from my_models import GEMINI_FLASH
from my_keys import GEMINI_API_KEY
from tavily_llm import web_search
from langgraph.prebuilt import create_react_agent

llm = ChatGoogleGenerativeAI(
            api_key=GEMINI_API_KEY,
            model=GEMINI_FLASH
        )

tools = [web_search]

llm_with_tools = llm.bind(tools = tools)

prompt_model = PromptTemplate(
    template="Me diga quais os impactos da IA no assunto {assunto}",
    input_variables=["assunto"]
)

# chain = prompt_model | llm | StrOutputParser()
chain = prompt_model | llm_with_tools | StrOutputParser()

resposta = chain.invoke({"assunto": "Agricultura"})

print(resposta)