import blocos.blocos_txt as bloc
import os

def main():
    indice = 0
    print("\n=== Leitura Braille Iniciada ===")

    if not bloc.gerar_bloco_numerico_por_indice(indice):
        print("Não há conteúdo para exibir.")
        return

    try:
        while True:
            print("\nDigite 1 para repetir o bloco, 2 para avançar, 0 para sair.")
            try:
                x = int(input("Escolha: "))
                if x == 1:
                    bloc.gerar_bloco_numerico_por_indice(indice)
                elif x == 2:
                    indice += 1
                    if not bloc.gerar_bloco_numerico_por_indice(indice):
                        print("\nFim do livro.")
                        break
                elif x == 0:
                    print("\nSaindo da leitura.")
                    break
                else:
                    print("Opção inválida.")
            except ValueError:
                print("Digite um número válido.")
    finally:
        try:
            os.remove("atual.txt")
            print("\nArquivo 'atual.txt' removido.")
        except FileNotFoundError:
            print("\nArquivo 'atual.txt' não encontrado para remover.")

if __name__ == "__main__":
    main()