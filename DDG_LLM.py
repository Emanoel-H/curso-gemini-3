import requests
from bs4 import BeautifulSoup
from ddgs import DDGS
import re

ddg = DDGS()

cidade = "Belém"

query = f"""
Liste os 5 principais restaurantes em {cidade}, segundo avaliações recentes no TripAdvisor ou sites similares de turismo.
Para cada restaurante, informe:
- Tipo de culinária (ex: regional, italiana, japonesa)
- Uma breve descrição (máx. 2 linhas)
- Avaliação média (se disponível)
- Faixa de preço

Responda apenas com dados atualizados e relevantes para turistas.
"""


def search(query, max_results=6):
    try:
        results = ddg.text(query, max_results=max_results)
        return [i["href"] for i in results]
    except Exception as e:
        raise e


for link in search(query):
    print(link)