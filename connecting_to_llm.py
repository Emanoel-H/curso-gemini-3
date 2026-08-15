from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from my_models import GEMINI_FLASH
from my_keys import GEMINI_API_KEY

llm = ChatGoogleGenerativeAI(
            api_key=GEMINI_API_KEY,
            model=GEMINI_FLASH
        )

prompt_model = PromptTemplate(
    template="Me diga quais os impactos da IA no assunto {assunto}",
    input_variables=["assunto"]
)

chain = prompt_model | llm | StrOutputParser()

resposta = chain.invoke({"assunto": "Agricultura"})

print(resposta)