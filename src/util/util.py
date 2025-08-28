import time
from src.mapping import map_carac as mp

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
        return [1, 1, 1, 1, 1, 1] 
    
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
            
                numeros_lista = [conversao_pinos(c) for c in palavra]
                mostrar_letra_por_letra(numeros_lista)

                verificar_rep_palavra(numeros_lista)

                indice += 1
                time.sleep(1)  
    except Exception as e:
        print(f"Erro ao processar o livro: {e}")

def mostrar_letra_por_letra(pinos_lista):
    """
    Exibe as letras em Braille, letra por letra.
    Para números, mostra o indicador uma única vez antes da sequência.
    """

    in_number_mode = False  

    for pinos in pinos_lista:
        if pinos == [1, 1, 1, 1, 1, 1]:
            in_number_mode = False  
            print("1 1 1 1 1 1", end="\r")
            time.sleep(2)
        elif isinstance(pinos, list) and len(pinos) == 2 and all(isinstance(p, list) for p in pinos):
            if not in_number_mode:
                indicador = pinos[0]
                print(" ".join(str(p) for p in indicador), end="\r")
                time.sleep(1.5)

                print("      ", end="\r")
                time.sleep(0.5)

                in_number_mode = True  
            numero = pinos[1]
            print(" ".join(str(p) for p in numero), end="\r")
            time.sleep(2)
        else:
            in_number_mode = False  
            print(" ".join(str(p) for p in pinos), end="\r")
            time.sleep(2)
    print() 

def verificar_rep_palavra(palavraBraileana):
    """
        Repete a palavra novamente
    """

    repeticao = input()

    while repeticao == "rep":
        mostrar_letra_por_letra(palavraBraileana)
        repeticao = input()