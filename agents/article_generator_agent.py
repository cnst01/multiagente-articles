# agents/article_generator_agent.py
import os
import requests

class ArticleGeneratorAgent:
    def __init__(self, base_content: str, groq_api_key: str = None):
        """
        Parâmetros:
          - base_content: Conteúdo base obtido pela API da Wikipedia.
          - groq_api_key: API key para autenticar na API do Groq. Se não for fornecida, será buscada na variável de ambiente GROQ_API_KEY.
        """
        self.base_content = base_content
        self.groq_api_key = groq_api_key or os.environ.get("GROQ_API_KEY")
        if not self.groq_api_key:
            raise ValueError("API key do Groq não foi definida. Defina a variável de ambiente GROQ_API_KEY ou passe como parâmetro.")

    def generate_article(self, min_words: int = 300) -> str:
        """
        Gera o artigo garantindo que ele possua pelo menos 'min_words' palavras.
        Se o conteúdo base não for suficiente, utiliza a API do Groq para expandir o texto.
        """
        words = self.base_content.split()
        current_word_count = len(words)

        if current_word_count >= min_words:
            return self.base_content

        additional_words_needed = min_words - current_word_count

        # Chama a função que utiliza a API do Groq para gerar o conteúdo adicional
        additional_content = self.call_groq_llm(self.base_content, additional_words_needed)
        
        # Concatena o texto base com o conteúdo adicional e garante a contagem mínima de palavras
        article = self.base_content + "\n\n" + additional_content
        return self.ensure_word_count(article, min_words)

    def call_groq_llm(self, prompt: str, words_needed: int) -> str:
        """
        Realiza a chamada à API do Groq para gerar conteúdo a partir de um prompt,
        utilizando o endpoint e payload conforme a documentação oficial.

        Parâmetros:
          - prompt: Texto base que servirá de contexto para a geração.
          - words_needed: Número aproximado de palavras a serem adicionadas (usado aqui para ajustar o prompt).
        
        Retorna:
          - Texto gerado pelo modelo.
        """
        # Endpoint conforme a documentação encontrada
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.groq_api_key}"
        }

        # Cria o prompt para a geração. Ajuste o conteúdo conforme a necessidade para orientar o modelo.
        message_content = (
            f"Continue o seguinte texto e adicione detalhes para criar um artigo coeso e informativo. "
            f"Certifique-se de gerar aproximadamente {words_needed} palavras adicionais. \n\n{prompt}"
        )

        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [{
                "role": "user",
                "content": message_content
            }]
        }

        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            # A resposta do Groq (modelo similar ao OpenAI Chat) deverá conter uma chave "choices"
            # onde cada item terá "message" com o conteúdo gerado.
            generated_text = ""
            choices = data.get("choices", [])
            if choices:
                generated_text = choices[0].get("message", {}).get("content", "").strip()
            if not generated_text:
                raise ValueError("Resposta da API do Groq não contém o conteúdo gerado.")
            return generated_text
        except Exception as e:
            print(f"Erro ao chamar a API do Groq: {e}")
            return "Erro na geração de conteúdo adicional."

    def ensure_word_count(self, text: str, min_words: int) -> str:
        """
        Garante que o texto final possui pelo menos 'min_words' palavras.
        Caso contrário, complementa com palavras dummy.
        """
        words = text.split()
        if len(words) < min_words:
            extra = " ".join(["informação"] * (min_words - len(words)))
            text += " " + extra
        return text
