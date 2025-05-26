import blocos.blocos_txt as bloc
import os

def main():
    indice = 0
    if not bloc.gerar_bloco_numerico_por_indice(indice):
        print("Não há conteúdo para exibir.")
        exit()

    try:
        while True:
            try:
                x = int(input("Digite 1 para retroceder, 2 para avançar: "))
                if x == 1:
                    if indice > 0:
                        indice -= 1
                    else:
                        print("\nInício do Livro")
                elif x == 2:
                    indice += 1
                else:
                    print("Opção inválida")
                    continue

                if not bloc.gerar_bloco_numerico_por_indice(indice):
                    print("\nFim do livro")
                    break
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

# import os
# import blocos.blocos_txt as bloc

# # ===== Execução principal =====

# if not os.path.exists("blocos.txt"):
#     # bloc.gerar_blocos_string("livro.txt")
#     bloc.gerar_blocos_inteiro("livro.txt")

# bloc.mostrar_bloco_atual()

# while True:
#     try:
#         x = int(input("Digite 1 para retroceder, 2 para avançar: "))
#         if x == 1:
#             bloc.retroceder()
#         elif x == 2:
#             if not bloc.avancar():
#                 break
#         else:
#             print("Opção inválida")
#     except ValueError:
#         print("Digite um número válido.")