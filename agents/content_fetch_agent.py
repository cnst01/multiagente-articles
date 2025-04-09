# agents/content_fetch_agent.py
import requests


class ContentFetchAgent:
    def __init__(self, topic: str):
        self.topic = topic

    def fetch_content(self) -> str:
        """
        Consulta a API da Wikipedia para obter o conteúdo do tópico.
        """
        url = "https://pt.wikipedia.org/w/api.php"
        params = {
            "action": "query",
            "prop": "extracts",
            "exlimit": "1",
            "explaintext": "1",
            "titles": self.topic,
            "format": "json",
            "utf8": "1",
            "redirects": "1"
        }
        response = requests.get(url, params=params)
        data = response.json()

        # A estrutura retornada contém um dicionário com as páginas
        pages = data.get("query", {}).get("pages", {})
        if pages:
            # Pega o primeiro resultado disponível
            page = next(iter(pages.values()))
            return page.get("extract", "Nenhum conteúdo encontrado.")
        return "Nenhum conteúdo encontrado."
