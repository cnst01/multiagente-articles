# Multiagente de Criação de Artigos com CrewAI

Este projeto demonstra um sistema multiagente utilizando CrewAI para automatizar a criação de artigos para um website. O sistema gera artigos com no mínimo 300 palavras sobre um determinado assunto, utilizando a API da Wikipedia para obter informações relevantes e LLMs para expandir o conteúdo.

## Funcionalidades

- **Agente de Conteúdo:** Consulta a API da Wikipedia para obter um extrato textual do tópico.
- **Agente de Geração de Artigos:** Expande o texto para garantir que o artigo contenha pelo menos 300 palavras (simulação de LLMs, podendo ser substituída por Groq ou Gemini).
- **API com FastAPI:** Permite a execução do sistema via um endpoint.
- **Output Formatado com Pydantic:** As respostas são estruturadas conforme o modelo definido.

## Tecnologias Utilizadas

- Python 3.9+
- CrewAI e CrewAI-tools (personalizado para consulta à Wikipedia)
- FastAPI e Uvicorn
- Requests
- Pydantic

## Estrutura do Projeto

multiagente-articles/ ├── agents/ │ ├── init.py │ ├── article_generator_agent.py │ └── content_fetch_agent.py ├── main.py └── README.md


## Instruções de Instalação e Execução

1. **Clone o repositório:**
   
   git clone <URL_DO_REPOSITORIO>
   cd multiagente-articles

2. **Crie e ative um ambiente virtual:**

    python -m venv venv
    source venv/bin/activate  # No Linux/macOS
    

3. **Instale as dependências:**

    pip install fastapi uvicorn requests

4. **Inicie o servidor:**

    uvicorn main:app --reload

5. **Utilize a API:**

    Abra o seu navegador e acesse a documentação interativa da API:

    http://127.0.0.1:8000/docs

    Para gerar um artigo, envie uma requisição GET para:

    /generate_article?topic=Futebol

