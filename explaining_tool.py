from lang_chain import cadeia
from langchain.tools import BaseTool
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models import ChatGoogleGenerativeAI
from my_models import GEMINI_FLASH
from my_keys import GEMINI_API_KEY
import ast

class ExplainingTool(BaseTool):
    name:str = "Explaining Tool"
    description:str = """
    Utilize esta ferramenta sempre que for solicitado que 
    você explique um conteúdo para pessoas.
    
    # Entrada Requerida
    - 'tema' (str) : Tema principal informado na pergunta do usuário.
    """

    return_direct: bool = True

    def _run(self, acao):
        acao = ast.literal_eval(acao)
        tema = acao.get("tema", "")

        llm = ChatGoogleGenerativeAI(
            api_key=GEMINI_API_KEY,
            model=GEMINI_FLASH
        )

        template_resposta = PromptTemplate(
            template="""
            Assuma o papel de um professor preocupado com aspectos de didática do usuário.
            
            1. Elabora uma explicação sobre o tema {tema} que seja compreensível por
            estudantes na fase de conclusão do Ensino Médio.
            2.Utilize exemplos do cotidiano para tornar a explicação mais fácil.
            3. Caso sugira algum recurso para apoiar a explicação, lembre-se
            do cenário e contexto brasileiro.
            4. Caso você utilize um código, seja didático e utilize Java
            
            Tema Pergunta: {tema}
            """,
            input_variables=["tema"]
        )

        cadeia = template_resposta | llm | StrOutputParser()

        resposta = cadeia.invoke({"tema": tema})
        return resposta

