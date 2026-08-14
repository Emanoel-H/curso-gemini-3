from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from my_models import GEMINI_FLASH
from my_keys import GEMINI_API_KEY
from my_helper import encode_image
from pathlib import Path
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatGoogleGenerativeAI(
    api_key= GEMINI_API_KEY,
    model= GEMINI_FLASH
)

path_image = Path.home() / "Desktop" / "curso_gemini_3" / "images" / "exemplo_grafico.jpg"

image_64 = encode_image(path_image)

# pergunta = "Descreva a imagem: "

template_analisador = ChatPromptTemplate.from_messages(
    [
        ("system", """
        Assuma que você é um analisador de imagens. A sua tarefa principal
        consiste em analisar uma imagem e extrair informações importantes 
        de forma objetiva.
        
        # FORMATO DE SAÍDA
        Descrição da Imagem: 'Coloque a sua descrição da imagem aqui'
        Rótulos: 'Coloque uma lista com três termos chave separados por vírgula'
                
        """),
        ("user",
         [
        {
            "type" : "text",
            "text" : "Descreva a imagem: "
        },
        {
            "type" : "image_url",
            "image_url" : {"url":"data:image/jpeg;base64,{image_64}"}
        }
    ])
    ]
)

cadeia = template_analisador | llm | StrOutputParser()

resposta = cadeia.invoke({"image_64": image_64})
print(resposta)

# mensagem = HumanMessage(
#     content= [
#         {
#             "type" : "text",
#             "text" : pergunta
#         },
#         {
#             "type" : "image_url",
#             "image_url" : f"data:image/jpeg;base64,{image_64}"
#         }
#     ]
# )

# resposta = llm.invoke([mensagem])

