import time
import arquivo.arq as arq
import mapeamento.map_carac as mp

def converter_para_pinos(texto):
    resultado = []
    palavra = []

    for c in texto:
        if mp.is_esta(c):
            pinos = mp.conversao_pinos(c)
            palavra.append(pinos)
        elif c.isspace():
            resultado.extend(palavra)
            resultado.append([0, 0, 0, 0, 0, 0])
            palavra = []

    if palavra:
        resultado.extend(palavra)

    return resultado

def mostrar_letra_por_letra(pinos_lista):
    for pinos in pinos_lista:
        if pinos == [0, 0, 0, 0, 0, 0]:
            print("0 0 0 0 0 0", end="\r")
        else:
            print(" ".join(str(p) for p in pinos), end="\r")
        time.sleep(2)
    print("0 0 0 0 0 0")  # final do bloco com zeros (espaço em branco)

def gerar_bloco_numerico_por_indice(indice):
    bloco = arq.ler_bloco("livro.txt", indice)

    if bloco is None or bloco.strip() == "":
        return False

    numeros_lista = converter_para_pinos(bloco)
    numeros_str = "\n".join("".join(str(p) for p in pinos) for pinos in numeros_lista)
    arq.salvar_texto("atual.txt", numeros_str)

    print(f"\n=== Bloco {indice} (Palavra: '{bloco}') ===")
    mostrar_letra_por_letra(numeros_lista)

    return True