import time
import util 

def processar_livro_por_palavra(caminho):
    """
    Processa o livro palavra por palavra e converte para Braille.
    Cada palavra é exibida na tela como um conjunto de pinos Braille.
    """
    try:
        with open(caminho, 'r', encoding="utf-8") as f:
            indice = 0
            for palavra in f.read().split():
                print(f"\n=== Processando Palavra {indice}: '{palavra}' ===")
                # Processar a palavra para Braille
                numeros_lista = converter_para_pinos(palavra)
                mostrar_letra_por_letra(numeros_lista)

                indice += 1
                time.sleep(1)  # Pausar entre as palavras para evitar sobrecarga
    except Exception as e:
        print(f"Erro ao processar o livro: {e}")


def converter_para_pinos(texto):
    """
    Converte uma palavra para o formato de Braille (em pinos).
    """
    # resultado = []
    # palavra = []

    # for c in texto:
    #     if is_esta(c):  # Verificar se o caractere é válido para Braille
    #         pinos = conversao_pinos(c)
    #         palavra.append(pinos)
    #     elif c.isspace():  # Espaço entre palavras
    #         resultado.extend(palavra)
    #         resultado.append([0, 0, 0, 0, 0, 0])  # Espaço representado como zeros
    #         palavra = []

    # if palavra:
    #     resultado.extend(palavra)

    # return resultado
    
    for c in texto:
        if util.is_in_caractere_map(c) or util.is_in_numeros_map(c):
            return util.conversao_pinos(c)
    
    return [1, 1, 1, 1, 1, 1] # Espaço representado como uns


def mostrar_letra_por_letra(pinos_lista):
    """
    Exibe as letras em Braille, letra por letra.
    """
    for pinos in pinos_lista:
        if pinos == [1, 1, 1, 1, 1, 1]:
            print("1 1 1 1 1 1", end="\r")  # Espaço
        else:
            print(" ".join(str(p) for p in pinos), end="\r")  # Mostra os pinos Braille
        time.sleep(2)  # Intervalo entre as letras
    # print("0 0 0 0 0 0")  # Final do bloco (representando o final do Braille)
    print("Ponto final :)")


if __name__ == "__main__":
    # Processar o livro "livro.txt"
    processar_livro_por_palavra("livro.txt")
