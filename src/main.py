from src.braille.processor import BrailleProcessor
from src.infrastructure.data_fetcher import DataFetcher

def main():
    fetcher = DataFetcher()
    processor = BrailleProcessor()

    try:
        dados = fetcher.fetch_data("https://api-login-ud37.onrender.com/text")
        processor.processar_livro_por_palavra(dados)
    except Exception as e:
        print(f"Erro na execução: {e}")

if __name__ == "__main__":
    main()
