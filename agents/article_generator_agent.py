import os
import requests

class ArticleGeneratorAgent:
    def __init__(self, base_content: str, groq_api_key: str = None):
        self.base_content = base_content
        self.groq_api_key = groq_api_key or os.environ.get("GROQ_API_KEY")
        if not self.groq_api_key:
            raise ValueError("API key do Groq não foi definida. Defina a variável de ambiente GROQ_API_KEY ou passe como parâmetro.")

    def generate_article(self, min_words: int = 300) -> str:
        words = self.base_content.split()
        current_word_count = len(words)

        # Se o conteúdo for muito grande (> 500 palavras), resumir
        if current_word_count > 500:
            # Pega apenas as primeiras 2000 palavras para evitar erro 413
            truncated_content = " ".join(words[:2000])
            summarized_content = self.call_groq_llm(truncated_content, action="summarize")
            return self.ensure_word_count(summarized_content, min_words)
        
        # Se o conteúdo for menor que o mínimo, expandir
        if current_word_count < min_words:
            additional_words_needed = min_words - current_word_count
            additional_content = self.call_groq_llm(self.base_content, action="expand", words_needed=additional_words_needed)
            article = self.base_content + "\n\n" + additional_content
            return self.ensure_word_count(article, min_words)
        
        # Se estiver entre min_words e 500 palavras, retorna o conteúdo original
        return self.base_content

    def call_groq_llm(self, prompt: str, action: str = "expand", words_needed: int = None) -> str:
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.groq_api_key}"
        }

        # Limita o tamanho do prompt para evitar erro 413
        prompt_words = prompt.split()
        if len(prompt_words) > 2000:
            prompt = " ".join(prompt_words[:2000]) + "\n\n[...continua...]"

        if action == "expand":
            message_content = (
                f"Continue o seguinte texto e adicione detalhes para criar um artigo coeso e informativo. "
                f"Gere aproximadamente {words_needed + 20} palavras adicionais. \n\n{prompt}"
            )
        elif action == "summarize":
            message_content = (
                f"Resuma o seguinte texto mantendo as informações mais importantes. "
                f"O resumo deve ter entre 200-400 palavras. \n\n{prompt}"
            )
        else:
            raise ValueError("Ação inválida. Use 'expand' ou 'summarize'.")

        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [{
                "role": "user",
                "content": message_content
            }],
            "max_tokens": 2000  # Limita o tamanho da resposta
        }

        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            generated_text = ""
            choices = data.get("choices", [])
            if choices:
                generated_text = choices[0].get("message", {}).get("content", "").strip()
            if not generated_text:
                raise ValueError("Resposta da API do Groq não contém o conteúdo gerado.")
            return generated_text
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 413:
                print("Erro: Conteúdo muito grande. Reduzindo o tamanho do prompt...")
                # Se ainda for grande, tenta com metade do texto
                reduced_prompt = " ".join(prompt.split()[:1000])
                return self.call_groq_llm(reduced_prompt, action, words_needed)
            else:
                print(f"Erro ao chamar a API do Groq: {e}")
                return "Erro na geração de conteúdo adicional."
        except Exception as e:
            print(f"Erro ao chamar a API do Groq: {e}")
            return "Erro na geração de conteúdo adicional."

    def ensure_word_count(self, text: str, min_words: int) -> str:
        words = text.split()
        if len(words) < min_words:
            extra = " ".join(["informação"] * (min_words - len(words)))
            text += " " + extra
        return text