#FastApi imports
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

#Pydantic validação automática de tipos
from pydantic import BaseModel

# Agente Gerador de artigo
from agents.article_generator_agent import ArticleGeneratorAgent

# Agente Buscador de Conteúdo na Wikipedia
from agents.content_fetch_agent import ContentFetchAgent

import os

#Lib para carregar de .env
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

app = FastAPI()

# Adiciona o middleware de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas as origens (para desenvolvimento)
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos HTTP
    allow_headers=["*"],  # Permite todos os cabeçalhos
)

class ArticleResponse(BaseModel):
    title: str
    content: str


@app.get("/generate_article", response_model=ArticleResponse)
async def generate_article(topic: str):
    """
    Endpoint que recebe o tópico e retorna o artigo gerado com no mínimo 300 palavras.
    """
    # Instancia o agente para buscar conteúdo na Wikipedia.
    content_agent = ContentFetchAgent(topic)
    base_content = content_agent.fetch_content()

    groq_api_key = os.environ.get("GROQ_API_KEY")
    if base_content == "Nenhum conteúdo encontrado." :
        article_agent = ArticleGeneratorAgent(topic, groq_api_key)
    else :
        # Instancia o agente para gerar/expandir o artigo.
        article_agent = ArticleGeneratorAgent(base_content, groq_api_key)
    article_text = article_agent.generate_article(min_words=300)

    return ArticleResponse(title=topic, content=article_text)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)