from tavily import TavilyClient
import re
from my_models import GEMINI_FLASH
from my_keys import TAVILY_API_KEY, GEMINI_API_KEY
import google.genai as genai

client = TavilyClient(api_key=TAVILY_API_KEY)
cidade = "Belém do Pará"

tavily_query = f"Restaurantes em {cidade} tripadvisor com maior quantidade de reviews e faixa de preço."

print("Iniciando Busca Agêntica por URLs do TripAdvisor com Tavily")
tripadvisor_url = None
try:
    tavily_results = client.search(query=tavily_query, max_results=5)

    if tavily_results and tavily_results["results"]:
        print(f"Tavily encontrou {len(tavily_results['results'])} resultados. Analisando...")

        for result in tavily_results["results"]:
            url = result["url"]

            if "tripadvisor.com" in url or "tripadvisor.com.br" in url:
                tripadvisor_url = url
                break

        if not tripadvisor_url:
            print("Nenhum URL relevante do Tripadvisor foi encontrado nos primeiros resultados.")
    else:
        print("Tavily não encontrou resultados para a busca agêntica.")

except Exception as e:
    print(f"Erro na busca agêntica com Tavily: {e}. Verifique sua chave API ou conexão.")

if tripadvisor_url:
    clean_url = re.sub(r'-o\d+-', '-', tripadvisor_url)
    tripadvisor_url = clean_url
    print(f"✅ URL encontrada limpa de paginação.")

print("-" * 50)
print(f"URL Final do Tripadvisor para raspagem: {tripadvisor_url if tripadvisor_url else 'NÃO ENCONTRADO'}")
print("-" * 50)