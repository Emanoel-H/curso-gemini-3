from tavily import TavilyClient
from my_models import GEMINI_FLASH
from my_keys import TAVILY_API_KEY, GEMINI_API_KEY
import google.genai as genai

client = TavilyClient(api_key=TAVILY_API_KEY)

result = client.search("O que são os multiagentes de Inteligência Artificial?", include_answer=True)

print(result["answer"])