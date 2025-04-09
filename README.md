# Multiagente de Criação de Artigos com CrewAI

Este projeto demonstra um sistema multiagente utilizando CrewAI para automatizar a criação de artigos para um website. O sistema gera artigos com no mínimo 300 palavras sobre um determinado assunto, utilizando a API da Wikipedia para obter informações relevantes e LLMs para expandir o conteúdo.

## Funcionalidades

- **Agente de Conteúdo:** Consulta a API da Wikipedia e extrai o conteúdo textual do tópico.
- **Agente de Geração de Artigos:** Garante que o artigo tenha no mínimo 300 palavras, utilizando a API do Groq para expandir o texto caso necessário.
- **Integração com LLM:** Realiza a chamada ao modelo de linguagem (Groq) enviando um prompt e recebendo o conteúdo gerado.
- **API com FastAPI:** Exposição de um endpoint para geração do artigo.
- **Output Formatado com Pydantic:** Estrutura a resposta com modelos Pydantic.
- **Carregamento Seguro da API Key:** Utiliza o arquivo `.env` e a biblioteca `python-dotenv` para armazenar e carregar a API key.


## Tecnologias Utilizadas

- Python 3.9+
- [CrewAI](https://github.com/crew-ai/crew) e CrewAI-tools (personalizado para consulta à Wikipedia)
- FastAPI e Uvicorn
- Requests
- Pydantic
- python-dotenv

## Estrutura do Projeto

plaintext
multiagente-articles/
├── agents/
│   ├── __init__.py
│   ├── article_generator_agent.py
│   └── content_fetch_agent.py
├── .env
├── main.py
└── README.md


## Instruções de Instalação e Execução

1. **Clone o repositório:**
   
   git clone <URL_DO_REPOSITORIO>
   cd multiagente-articles

2. **Crie e ative um ambiente virtual:**

    python -m venv venv
    source venv/bin/activate  # No Linux/macOS
    

3. **Instale as dependências:**

    pip install fastapi uvicorn requests

4. Configure a API Key

    Crie um arquivo .env na raiz do projeto com o seguinte conteúdo:

    GROQ_API_KEY=suachaveaqui123456789

5. **Inicie o servidor:**

    uvicorn main:app --reload

6. **Utilize a API:**

    Abra o seu navegador e acesse a documentação interativa da API:

    http://127.0.0.1:8000/docs

    Para gerar um artigo, envie uma requisição GET para:

    /generate_article?topic=Futebol

## Detalhes da Implementação

**Integração com a API da Wikipedia**

    Arquivo: agents/content_fetch_agent.py

    Descrição: Consulta a API da Wikipedia e retorna um extrato em texto puro do tópico informado.

**Geração de Artigos com a LLM**

    Arquivo: agents/article_generator_agent.py

    Descrição:

        Garante que o artigo contenha no mínimo 300 palavras.

        Se necessário, expande o conteúdo utilizando a API do Groq (ou outro LLM) para gerar conteúdo adicional.

        A função call_groq_llm realiza a chamada autenticada à API, enviando o prompt e recuperando o texto gerado.

        A API key é carregada de forma segura via variável de ambiente, utilizando python-dotenv.

**Orquestração com FastAPI**

    Arquivo: main.py

    Descrição:

        Define o endpoint /generate_article que recebe o parâmetro topic.

        Instancia os agentes de conteúdo e de geração, integra suas funções e retorna o artigo formatado via Pydantic.

**Engenharia de Prompts**

O sistema utiliza técnicas de engenharia de prompts para:

    Instruir a LLM a expandir o texto da Wikipedia de maneira coesa.

    Definir no prompt a quantidade aproximada de palavras a serem adicionadas para atingir o mínimo exigido.

    Ajustar o modelo e os parâmetros de geração conforme o necessário, garantindo a qualidade e relevância do artigo.

**Contribuição**

Contribuições são bem-vindas! Por favor, abra issues e pull requests para melhorias e novas funcionalidades. Certifique-se de seguir as boas práticas de codificação e documentação.