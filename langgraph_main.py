from langgraph_components import Agent, AgentState
from my_models import GEMINI_FLASH
from my_keys import TAVILY_API_KEY, GEMINI_API_KEY
import google.genai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.tavily_search import TavilySearchResults
from IPython.display import Image, display



def main():
    prompt = """Você é um assistente de pesquisa inteligente. Use o mecanismo de busca para procurar informações. \
    Você tem permissão para fazer múltiplas chamadas (seja em conjunto ou em sequência). \
    Procure informações apenas quando tiver certeza do que você quer. \
    Se precisar pesquisar alguma informação antes de fazer uma pergunta de acompanhamento, você tem permissão para fazer isso!
    """

    tool = TavilySearchResults(max_results=4)

    model = ChatGoogleGenerativeAI(model=GEMINI_FLASH, temperature=0, api_key= GEMINI_API_KEY)

    abot = Agent(model, [tool], system=prompt)

    

    # mermaid_code = abot.graph.get_graph().draw_mermaid()
    #
    # print(mermaid_code)
    #
    # try:
    #     image_data = abot.graph.get_graph().draw_mermaid_png()
    #     display(Image(data=image_data))
    # except Exception as e:
    #     print(f"Erro ao tentar gerar PNG do Mermaid: {e}")
    #     print("\nCertifique-se de que a sua versão do LangGraph possui o método `.draw_mermaid_png()`.")
    #     print("Como alternativa, use `.draw_mermaid()` para obter a string e visualizar externamente.")
    # agent = Agent(system="Você é um assistente útil e objetivo")
    # print(agent("Hebrew prayers like: Baruch attah Adonai Elohinu Melech Haolam borei peri..."))

if __name__ == "__main__":
    main()