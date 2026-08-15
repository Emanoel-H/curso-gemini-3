from langchain.agents import AgentExecutor
from orchestrator import OrchestratorAgent

def main():
    agent = OrchestratorAgent()
    executor = AgentExecutor(
        agent=agent.agent,
        tools=agent.tools
    )

    pergunta = "Faça uma análise da imagem exemplo_grafico.jpg"
    resposta = executor.invoke({"input": pergunta})
    print(resposta)

if __name__ == "__main__":
    main()