import arquivo.arq as arq
import mapeamento.map_carac as mp

# ===== Geração inicial dos blocos a partir do livro.txt =====

def gerar_blocos_string(caminho):
    texto = arq.ler_texto_completo(caminho)
    blocos = []
    i = 0
    while i < len(texto):
        bloco = ""
        start_i = i
        while i < len(texto):
            palavra = ""
            while i < len(texto) and not texto[i].isspace():
                palavra += texto[i]
                i += 1

            espaco = ""
            while i < len(texto) and texto[i].isspace():
                espaco += texto[i]
                i += 1

            if len(palavra) > 20:
                if bloco == "":
                    bloco = palavra[:20]
                    i = start_i + 20
                break

            if len(bloco) + len(palavra) + len(espaco) <= 20:
                bloco += palavra + espaco
            else:
                i -= len(palavra + espaco)
                break

        blocos.append(bloco)

    # Salvar blocos
    with open("blocos.txt", "w", encoding="utf-8") as f:
        for bloco in blocos:
            f.write(bloco.replace("\n", " ") + "\n")
    
    with open("indice.txt", "w", encoding="utf-8") as f:
        f.write("0")

def gerar_blocos_inteiro(caminho="livro.txt"):

    # Gera os blocos de texto (salva em blocos.txt)
    gerar_blocos_string(caminho)

    # Agora lê os blocos gerados
    blocos = arq.ler_blocos()
    blocos_numericos = []

    for bloco in blocos:
        numeros = []
        for letra in bloco:
            if mp.is_esta(letra):
                numeros.append(str(mp.conversao_num(letra)))
        blocos_numericos.append(" ".join(numeros))

    # Salva os blocos numéricos
    with open("blocos_num.txt", "w", encoding="utf-8") as f:
        for bloco_num in blocos_numericos:
            f.write(bloco_num + "\n")

    print("Conversão concluída. Os blocos numéricos foram salvos em 'blocos_num.txt'.")

# ===== Exibição do bloco atual =====

def mostrar_bloco_atual():
    blocos = arq.ler_blocos()
    idx = arq.ler_indice()

    if idx < 0 or idx >= len(blocos):
        print("Fim ou início do livro\n")
        return

    bloco_atual = blocos[idx]
    bloco_proximo = blocos[idx+1] if idx+1 < len(blocos) else ""
    arq.salvar_bloco("atuais.txt", bloco_atual)
    arq.salvar_bloco("proximos.txt", bloco_proximo)

    print("\n=== Bloco Atual ===")
    print(bloco_atual)

# ===== Avançar e retroceder =====

def avancar():
    blocos = arq.ler_blocos()
    idx = arq.ler_indice()
    if idx >= len(blocos) - 1:
        print("Acabou o livro")
        return False
    arq.salvar_indice(idx + 1)
    mostrar_bloco_atual()
    return True

def retroceder():
    idx = arq.ler_indice()
    if idx == 0:
        print("Início do livro")
        return
    arq.salvar_indice(idx - 1)
    mostrar_bloco_atual()