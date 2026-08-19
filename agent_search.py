from tavily import TavilyClient
import re
from my_models import GEMINI_FLASH
from my_keys import TAVILY_API_KEY, GEMINI_API_KEY
import google.genai as genai
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from selenium.common.exceptions import WebDriverException, TimeoutException

def scrape_restaurantes_info(url):
    if not url:
        print("Erro: URL vazia ou não localizada para raspagem.")
        return None

    try:
        service = Service(ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126")

        driver = webdriver.Chrome(service=service, options=options)
        driver.set_page_load_timeout(30)
    except Exception as e:
        print(f"Erro ao inicializar o driver do Selenium: {e}")
        return None

    try:
        print(f"Tentando carregar a página com Selenium: {url}")
        driver.get(url)

        driver.implicitly_wait(10)

        response_text = driver.page_source
    except TimeoutException:
        print(f"Erro de tempo limite ao carregar página: {url}")
        return None
    except WebDriverException as e:
        print(f"Erro ao carregar a página {url} com Selenium: {e}. Pode ser um bloqueio ou problema de conexão.")
        return None
    finally:
        driver.quit()

    soup = BeautifulSoup(response_text, "html.parser")
    return soup

soup_tripadvisor = None

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

soup_tripadvisor = None

if 'tripadvisor_url' in locals() and tripadvisor_url:
    print(f"\nTentando raspar a página identificada: {tripadvisor_url}")
    soup_tripadvisor = scrape_restaurantes_info(tripadvisor_url)

    if soup_tripadvisor:
        print("HTML da página do Tripadvisor obtido com sucesso!")
        page_title_tag = soup_tripadvisor.find('title')
        if page_title_tag:
            print(f"Título da página: {page_title_tag.get_text(strip=True)}")
        else:
            print("Não foi possível encontrar o título da página.")
    else:
        print("Falha ao raspar página do Tripadvisor. Verifique o URL ou se o site está bloqueando.")

else:
    print("Não há URL no Tripadvisor válido para raspar (obtido no Bloco 1).")

print("-" * 50)