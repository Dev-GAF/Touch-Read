import time
from mapeamento import map_carac as mp

def is_in_caractere_map(carac):
    """
    Verifica se o caractere está presente no alfabeto (A–Z)
    """

    return carac.upper() in mp.caracteres or carac in mp.numeros

def is_space(carac):
    return carac == " "

def conversao_pinos(c: str):
    """
    Converte um caractere ou número para o formato de pinos Braille.
    O mapeamento é feito com base no alfabeto A-Z; 0-9.
    """
    if c.upper() in mp.caracteres:
        return mp.caracteres[c.upper()]
    elif c in mp.numeros:
        letra = mp.numeros[c]
        indicador_numeros = mp.indicador_numeros["#"]
        return [indicador_numeros, mp.caracteres[letra]]
    else:
        return [1, 1, 1, 1, 1, 1]  # caractere inválido ou espaço
    
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
                numeros_lista = [conversao_pinos(c) for c in palavra]
                mostrar_letra_por_letra(numeros_lista)

                indice += 1
                time.sleep(1)  # Pausar entre as palavras para evitar sobrecarga
    except Exception as e:
        print(f"Erro ao processar o livro: {e}")

def mostrar_letra_por_letra(pinos_lista):
    """
    Exibe as letras em Braille, letra por letra.
    Para números, mostra o indicador uma única vez antes da sequência.
    """
    in_number_mode = False  # Flag para saber se estamos em sequência numérica

    for pinos in pinos_lista:
        if pinos == [1, 1, 1, 1, 1, 1]:
            # Espaço ou caractere inválido
            in_number_mode = False  # Sai do modo número
            print("1 1 1 1 1 1", end="\r")
            time.sleep(2)

        elif isinstance(pinos, list) and len(pinos) == 2 and all(isinstance(p, list) for p in pinos):
            # Este é um número (lista de duas listas: [indicador, letra])

            if not in_number_mode:
                # Mostrar o indicador de número apenas no início
                indicador = pinos[0]
                print(" ".join(str(p) for p in indicador), end="\r")
                time.sleep(1.5)

                print("      ", end="\r")
                time.sleep(0.5)

                in_number_mode = True  # Entramos em modo número

            numero = pinos[1]
            print(" ".join(str(p) for p in numero), end="\r")
            time.sleep(2)

        else:
            # Letra normal
            in_number_mode = False  # Sai do modo número se estava
            print(" ".join(str(p) for p in pinos), end="\r")
            time.sleep(2)

    print()  # Final do bloco
