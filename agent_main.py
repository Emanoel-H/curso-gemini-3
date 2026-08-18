from storage_agent import run_react_agent

def iniciar_conversacao_com_agente():
    print("--- Agente de Inventário Interativo ---")
    print("Digite sua pergunta sobre o inventário, ou digite 'sair' para encerrar.")
    print("*" * 50)

    while True:
        pergunta_usuario = input("\nVocê: ")

        if pergunta_usuario.lower().strip() == 'sair':
            print("Encerrando a conversa. Até logo!")
            break

        print("\nAgente: Processando...")
        try:
            resposta_agente = run_react_agent(pergunta_usuario)
            print(f"\nAgente: {resposta_agente}")
        except Exception as e:
            print(f"\nAgente: Ocorreu um erro ao processar sua pergunta: {e}")
            print("Por favor, tente novamente ou digite 'sair'.")


if __name__ == "__main__":
    iniciar_conversacao_com_agente()
    pass