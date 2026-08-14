from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from my_models import GEMINI_FLASH
from my_keys import GEMINI_API_KEY
from my_helper import encode_image
from pathlib import Path
from langchain.prompts import ChatPromptTemplate

llm = ChatGoogleGenerativeAI(
    api_key= GEMINI_API_KEY,
    model= GEMINI_FLASH
)

path_image = Path.home() / "Desktop" / "curso_gemini_3" / "images" / "exemplo_grafico.jpg"

image_64 = encode_image(path_image)

pergunta = "Descreva a imagem: "

mensagem = HumanMessage(
    content= [
        {
            "type" : "text",
            "text" : pergunta
        },
        {
            "type" : "image_url",
            "image_url" : f"data:image/jpeg;base64,{image_64}"
        }
    ],
)

resposta = llm.invoke([mensagem])

print(resposta)