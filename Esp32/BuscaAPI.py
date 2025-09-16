import urequests

class buscaAPI:
    def __init__(self, url):
        self.url = url

    def get_texts(self):
        """Retorna todos os textos da API como lista"""
        try:
            response = urequests.get(self.url)
            data = response.json()
            response.close()  # sempre fechar para liberar memória
            return data.get("textos", [])
        except Exception as e:
            print("Erro ao acessar a API:", e)
            return []

    def get_texts_unified(self, separator=" "):
        """Retorna todos os textos concatenados em uma única string"""
        textos = self.get_texts()
        return separator.join(textos)
