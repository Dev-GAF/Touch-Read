import requests
import logging

class DataFetcher:
    def __init__(self, timeout=60):
        self.timeout = timeout
        self.logger = logging.getLogger(__name__)

    def fetch_data(self, url: str):
        """
        Faz uma requisição GET para a URL informada e retorna o JSON.
        """
        try:
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.HTTPError as e:
            self.logger.error(f"Erro HTTP na requisição: {e.response.status_code} - {e.response.reason}")
            raise
        except requests.RequestException as e:
            self.logger.error(f"Erro na requisição: {e}")
            raise
