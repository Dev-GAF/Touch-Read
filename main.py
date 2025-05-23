import os
import blocos.blocos_txt as bloc

# ===== Execução principal =====

if not os.path.exists("blocos.txt"):
    # bloc.gerar_blocos_string("livro.txt")
    bloc.gerar_blocos_inteiro("livro.txt")

bloc.mostrar_bloco_atual()

while True:
    try:
        x = int(input("Digite 1 para retroceder, 2 para avançar: "))
        if x == 1:
            bloc.retroceder()
        elif x == 2:
            if not bloc.avancar():
                break
        else:
            print("Opção inválida")
    except ValueError:
        print("Digite um número válido.")