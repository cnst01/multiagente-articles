# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from agents.article_generator_agent import ArticleGeneratorAgent
from agents.content_fetch_agent import ContentFetchAgent
import os
app = FastAPI()

from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()


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

    # Instancia o agente para gerar/expandir o artigo.
    groq_api_key = os.environ.get("GROQ_API_KEY")
    article_agent = ArticleGeneratorAgent(base_content, groq_api_key)
    article_text = article_agent.generate_article(min_words=300)

    return ArticleResponse(title=topic, content=article_text)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
