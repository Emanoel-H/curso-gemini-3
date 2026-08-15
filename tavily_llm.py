from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import tool
from my_keys import TAVILY_API_KEY

@tool
def web_search(query: str) -> list:

    """
    Busca na web por um termo específico.
    """

    tavily_search = TavilySearchResults(
        max_results=2,
        search_depth="advanced"
    )

    search_result = tavily_search.invoke(query)
    return search_result

resultado = web_search.invoke("IA na Agricultura")

print(resultado)