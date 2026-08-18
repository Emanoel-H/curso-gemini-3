from typing_extensions import TypedDict
import google.genai as genai
import re
from my_models import GEMINI_FLASH
from my_keys import GEMINI_API_KEY


PROMPT_REACT = """
Você funciona em um ciclo de Pensamento, Ação, Pausa e Observação.
Ao final do ciclo, você fornece uma Resposta.
Use "Pensamento" para descrever seu raciocínio.
Use "Ação" para executar ferramentas - e então retorne "PAUSA".
A "Observação" será o resultado da ação executada.
Ações disponíveis:
    - consultar_estoque: retorna a quantidade disponível de um item no inventário (ex: "consultar_estoque: teclado")
    - consultar_preco_produto: retorna o preço unitário de um produto (ex: "consultar_preco_produto: mouse gamer")
    - consultar_produto_mais_caro: retorna o preço e o nome do produto 
      mais caro do estoque (ex: "consultar_produto_mais_caro: monitor R$ 50.00") 
    - calcular_valor_total_lista: calcula o valor total de uma lista de itens de compra. Recebe uma string com itens separados por virgula.

Exemplo:
Pergunta: Quantos monitores temos em estoque?
Pensamento: Devo consultar a ação consultar_estoque para saber a quantidade de monitores.
Ação: consultar_estoque: monitor
PAUSA

Observação: Temos 75 monitores em estoque.
Resposta: Há 75 monitores em estoque.
""".strip()

class AgentState(TypedDict):
    pergunta: str
    historico: list[str]
    acao_pendente: str
    resposta_final: str

def consultar_estoque(item: str) -> str:
    item = item.lower()
    estoque = {
        "monitor": 75,
        "teclado": 120,
        "mouse gamer": 80,
        "webcam": 40,
        "headset": 60,
        "impressora": 15
    }

    if item in estoque:
        return f"Temos {estoque[item]} {item}s em estoque."
    else:
        return f"Item '{item}' não encontrado no inventário."

def consultar_preco_produto(produto: str) -> str:
    produto = produto.lower()
    precos = {
        "monitor": 999.90,
        "teclado": 150.00,
        "mouse gamer": 99.50,
        "webcam": 120.00,
        "headset": 180.00,
        "impressora": 750.00
    }

    if produto in precos:
        return f"O preço de um(a) {produto} é R$ {precos[produto]:.2f}."
    else:
        return f"Produto '{produto}' não encontrado na lista de preços."

def consultar_produto_mais_caro() -> str:
    preco_mais_alto = 0
    produto_mais_caro = ""

    precos = {
        "monitor": 999.90,
        "teclado": 150.00,
        "mouse gamer": 99.50,
        "webcam": 120.00,
        "headset": 180.00,
        "impressora": 750.00
    }

    for produto in precos:
        if precos[produto] >= preco_mais_alto:
            preco_mais_alto = precos[produto]
            produto_mais_caro = produto

    return f"O produto mais caro é o {produto_mais_caro}, custando R${preco_mais_alto:.2f}."


def calcular_valor_total_lista(lista_itens: str) -> str:
    precos_do_inventario = {
        "monitor": 999.90,
        "teclado": 150.00,
        "mouse gamer": 99.50,
        "webcam": 120.00,
        "headset": 180.00,
        "impressora": 750.00
    }

    itens_processados = [item.strip().lower() for item in lista_itens.split(',')]

    valor_total = 0.0
    itens_nao_encontrados = []
    itens_encontrados = []
    resposta = ""

    for item in itens_processados:
        if item in precos_do_inventario:
            valor_total += precos_do_inventario[item]
            itens_encontrados.append(item)
        else:
            itens_nao_encontrados.append(item)

    if valor_total != 0:
        for item in itens_encontrados:
            if item in precos_do_inventario:
                resposta += f"Produto: {item} | Preço: R$ {precos_do_inventario[item]:.2f}\n"

    resposta += f"O valor total dos itens encontrados é R$ {valor_total:.2f}."
    if itens_nao_encontrados:
        resposta += f"\nOs seguintes itens não foram encontrados e não foram incluídos no cálculo: {', '.join(itens_nao_encontrados)}"

    return resposta

print(consultar_estoque("teclado"))
print(consultar_preco_produto("mouse gamer"))

def run_react_agent(pergunta: str, max_iterations: int = 5) -> str:
    client = genai.Client(api_key=GEMINI_API_KEY)
    client.models.GEMINI_FLASH = GEMINI_FLASH

    chat = client.chats.create(model=GEMINI_FLASH)

    chat.send_message(PROMPT_REACT)

    current_prompt = pergunta

    for i in range(max_iterations):
        response = chat.send_message(current_prompt)
        response_text = response.text.strip()

        print(f"--- Iteração {i + 1} ---")
        print(f"Modelo pensou/respondeu:\n{response_text}\n")

        if response_text.startswith("Resposta:"):
            return response_text.replace("Resposta:", "").strip()

        # match = re.search(r"Ação:\s*(\w+)\s*\[\s*(.*)\s*\]", response_text)
        match = re.search(r"Ação:\s*(\w+):\s*(.+)", response_text)

        if match:
            action_name = match.group(1).strip()
            action_arg = match.group(2).strip()

            observacao = ""
            if action_name == "consultar_estoque":
                observacao = consultar_estoque(action_arg)
            elif action_name == "consultar_preco_produto":
                observacao = consultar_preco_produto(action_arg)
            elif action_name == "consultar_produto_mais_caro":
                observacao = consultar_produto_mais_caro()
            elif action_name == "calcular_valor_total_lista":
                observacao = calcular_valor_total_lista(action_arg)
            else:
                observacao = f"Erro: Ação '{action_name}' desconhecida."

            current_prompt = f"Observação: {observacao}\nResposta:"

            print(f"Executou ação: {action_name}({action_arg})")
            print(f"Observação: {observacao}\n")

        else:
            return f"Erro: O agente não conseguiu extrair uma Ação ou Resposta final após {i + 1} iterações. Última resposta: {response_text}"

    return "Erro: Limite máximo de iterações atingido sem uma resposta final."

pergunta_1 = "Quantos mouses gamers estão no inventário?"
print(f"**Interação 1: {pergunta_1}**")
resposta_1 = run_react_agent(pergunta_1)
print(f"\n**RESPOSTA FINAL DO AGENTE 1:** \n{resposta_1}\n")

print("\n" + "=" * 50 + "\n")

pergunta_2 = "Quanto custa uma impressora?"
print(f"**Interação 2: {pergunta_2}**")
resposta_2 = run_react_agent(pergunta_2)
print(f"\nRESPOSTA FINAL DO AGENTE 2:** \n{resposta_2}\n")

print("\n" + "=" * 50 + "\n")

pergunta_3 = "Tem cadeira no estoque?"
print(f"**Interação 3: {pergunta_3}**")
resposta_3 = run_react_agent(pergunta_3)
print(f"\nRESPOSTA FINAL DO AGENTE 3:** \n{resposta_3}\n")

print("\n" + "=" * 50 + "\n")

pergunta_4 = "Qual o produto mais caro do estoque?"
print(f"**Interação 4: {pergunta_4}**")
resposta_4 = run_react_agent(pergunta_4)
print(f"\nRESPOSTA FINAL DO AGENTE 4:** \n{resposta_4}\n")

print("\n" + "=" * 50 + "\n")

pergunta_5 = "Qual o valor de um teclado, uma impressora e uma webcam?"
print(f"**Interação 5: {pergunta_5}**")
resposta_5 = run_react_agent(pergunta_5)
print(f"\nRESPOSTA FINAL DO AGENTE 5:** \n{resposta_5}\n")

print("\n" + "=" * 50 + "\n")