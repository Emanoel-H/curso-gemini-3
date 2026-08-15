from pydantic import BaseModel, Field
from typing import List

class ModelImageDetails(BaseModel):
    titulo:str = Field(
        description= "Defina o título adequado para a imagem analisada."
    )

    descricao:str = Field(
        description= "Coloque aqui uma descrição detalhada de sua análise para imagem."
    )

    rotulos:List[str] = Field(
        description= "Defina três rótulos principais para a imagem analisada."
    )