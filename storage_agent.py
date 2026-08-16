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