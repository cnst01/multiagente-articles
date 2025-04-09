# agents/article_generator_agent.py
class ArticleGeneratorAgent:
    def __init__(self, base_content: str):
        self.base_content = base_content

    def generate_article(self, min_words: int = 300) -> str:
        """
        Garante que o artigo possua pelo menos 'min_words' palavras.
        Se o conteúdo base não for suficiente, expande o texto utilizando uma simulação de LLM.
        """
        words = self.base_content.split()
        current_word_count = len(words)

        if current_word_count >= min_words:
            return self.base_content

        additional_words_needed = min_words - current_word_count
        additional_content = self.simulate_llm_generation(self.base_content, additional_words_needed)

        article = self.base_content + "\n\n" + additional_content
        return self.ensure_word_count(article, min_words)

    def simulate_llm_generation(self, prompt: str, words_needed: int) -> str:
        """
        Simula a geração de conteúdo usando um LLM.
        Na prática, você substituirá esta função pela chamada à API do LLM de sua escolha.
        """
        # Exemplo de texto adicional – repete uma mensagem para atingir o número de palavras desejado.
        base_sentence = (
            "Este artigo fornece uma visão detalhada sobre o assunto abordado, "
            "apresentando informações adicionais, análises históricas, e contextos atuais. "
        )
        # Estimativa de palavras por repetição da frase
        words_per_sentence = len(base_sentence.split())
        repetitions = (words_needed // words_per_sentence) + 1

        return " ".join([base_sentence] * repetitions)

    def ensure_word_count(self, text: str, min_words: int) -> str:
        """
        Caso o texto final ainda possua menos que min_words, complementa com palavras dummy.
        """
        words = text.split()
        if len(words) < min_words:
            extra = " ".join(["informação"] * (min_words - len(words)))
            text += " " + extra
        return text
