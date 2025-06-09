import arquivo.arq as arq
import mapeamento.map_carac as mp

def extrair_bloco(texto, indice, tamanho_bloco=20):
    i = 0
    blocos = []

    while i < len(texto):
        bloco = ""
        while i < len(texto):
            palavra = ""
            while i < len(texto) and not texto[i].isspace():
                palavra += texto[i]
                i += 1

            espaco = ""
            while i < len(texto) and texto[i].isspace():
                espaco += texto[i]
                i += 1

            if len(palavra) > tamanho_bloco:
                if bloco == "":
                    bloco = palavra[:tamanho_bloco]
                    texto = palavra[tamanho_bloco:] + espaco + texto[i:]
                    i = 0
                break

            if len(bloco) + len(palavra) + len(espaco) <= tamanho_bloco:
                bloco += palavra + espaco
            else:
                i -= len(palavra + espaco)
                break

        blocos.append(bloco.strip())

    if indice < 0 or indice >= len(blocos):
        return None

    return blocos[indice]

def converter_para_pinos(texto):
    resultado = []
    for c in texto:
        if mp.is_esta(c):
            pinos = mp.conversao_pinos(c)
            resultado.append("".join(str(p) for p in pinos))  # Junta os 6 pinos em uma string só
    return " ".join(resultado)

def gerar_bloco_numerico_por_indice(indice):
    texto = arq.ler_texto_completo("livro.txt")
    bloco = extrair_bloco(texto, indice)

    if bloco is None:
        return False

    numeros = converter_para_pinos(bloco)
    arq.salvar_texto("atual.txt", numeros)

    print("\n=== Bloco Atual ===")
    print(numeros)

    return True