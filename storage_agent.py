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
