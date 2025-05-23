# import os

# # Função para ler o texto completo do arquivo
# def ler_texto_completo(caminho):
#     with open(caminho, "r", encoding="utf-8") as f:
#         return f.read()

# def salvar_bloco(nome, conteudo):
#     with open(nome, "w", encoding="utf-8") as f:
#         f.write(conteudo)

# def ler_bloco(nome):
#     try:
#         with open(nome, "r", encoding="utf-8") as f:
#             return f.read()
#     except FileNotFoundError:
#         return ""

# def excluir_arquivos():
#     try:
#         os.remove("atuais.txt")
#         os.remove("proximos.txt")
#         os.remove("lidos.txt")
#         print("Arquivos excluídos com sucesso!")
#     except Exception as e:
#         print(f"Erro ao excluir arquivos: {e}")

# def avancar_bloco():

#     caminho_original = "livro.txt"
#     texto = ler_texto_completo(caminho_original)

#     lidos = ler_bloco("lidos.txt")
#     posicao_atual = len(lidos)

#     restante = texto[posicao_atual:]

#     if not restante:
#         print("Acabou o livro\n")
#         excluir_arquivos()
#         return 0

#     bloco_atual = ""
#     i = 0

#     while i < len(restante):
#         palavra = ""
#         while i < len(restante) and not restante[i].isspace():
#             palavra += restante[i]
#             i += 1

#         espaco = ""
#         while i < len(restante) and restante[i].isspace():
#             espaco += restante[i]
#             i += 1

#         # Palavra inteira maior que 20, precisa ser quebrada
#         if len(palavra) > 20:
#             if bloco_atual == "":
#                 bloco_atual = palavra[:20]
#                 restante_novo = palavra[20:] + espaco + restante[i:]
#             else:
#                 i -= len(palavra + espaco)
#             break

#         # Verifica se cabe no bloco
#         if len(bloco_atual) + len(palavra) + len(espaco) <= 20:
#             bloco_atual += palavra + espaco
#         else:
#             i -= len(palavra + espaco)
#             break

#     # Define novo conteúdo lido e restante
#     novo_lidos = texto[:posicao_atual + len(bloco_atual)]
#     restante_novo = texto[posicao_atual + len(bloco_atual):]

#     bloco_proximo = restante_novo[:20]

#     salvar_bloco("atuais.txt", bloco_atual)
#     salvar_bloco("proximos.txt", bloco_proximo)
#     salvar_bloco("lidos.txt", novo_lidos)

#     print("\n=== Bloco Atual ===")
#     print(bloco_atual)

#     print()
#     return 1, bloco_atual, novo_lidos, bloco_proximo

# def retroceder_bloco():
#     caminho_original = "livro.txt"
#     texto = ler_texto_completo(caminho_original)
#     lidos = ler_bloco("lidos.txt")
#     posicao_atual = len(lidos)

#     if posicao_atual == 0:
#         print("Início do livro\n")
#         return

#     # Reprocessa todo o texto em blocos
#     blocos = []
#     i = 0
#     while i < len(texto):
#         bloco = ""
#         start_i = i
#         while i < len(texto):
#             palavra = ""
#             while i < len(texto) and not texto[i].isspace():
#                 palavra += texto[i]
#                 i += 1

#             espaco = ""
#             while i < len(texto) and texto[i].isspace():
#                 espaco += texto[i]
#                 i += 1

#             if len(palavra) > 20:
#                 if bloco == "":
#                     bloco = palavra[:20]
#                     i = start_i + 20
#                 break

#             if len(bloco) + len(palavra) + len(espaco) <= 20:
#                 bloco += palavra + espaco
#             else:
#                 i -= len(palavra + espaco)
#                 break

#         blocos.append(bloco)

#     # Reconstrói o conteúdo lido até agora
#     conteudo_lido = "".join(blocos)
#     acumulado = 0
#     indice_atual = 0
#     for idx, bloco in enumerate(blocos):
#         acumulado += len(bloco)
#         if acumulado >= posicao_atual:
#             indice_atual = idx
#             break

#     if indice_atual == 0:
#         print("Início do livro\n")
#         return

#     # Retrocede um bloco
#     bloco_anterior = blocos[indice_atual - 1]
#     novos_lidos = "".join(blocos[:indice_atual - 1])
#     bloco_atual = bloco_anterior
#     proximo_bloco = blocos[indice_atual] if indice_atual < len(blocos) else ""

#     salvar_bloco("atuais.txt", bloco_atual)
#     salvar_bloco("proximos.txt", proximo_bloco)
#     salvar_bloco("lidos.txt", novos_lidos)

#     print("\n=== Bloco Anterior ===")
#     print(bloco_atual)

# # Primeira execução
# avancar_bloco()

# # Loop contínuo
# while True:
#     x = int(input("Digite 1 para retroceder, 2 para avançar: "))

#     if x == 1:
#         retroceder_bloco()
#     elif x == 2:
#         if avancar_bloco() == 0:
#             break
#     else:
#         print("Opção inválida")

import os

# ===== Funções de leitura e escrita básicas =====

def ler_texto_completo(caminho):
    with open(caminho, "r", encoding="utf-8") as f:
        return f.read()

def salvar_bloco(nome, conteudo):
    with open(nome, "w", encoding="utf-8") as f:
        f.write(conteudo)

def ler_blocos():
    with open("blocos.txt", "r", encoding="utf-8") as f:
        return f.read().splitlines()

def ler_indice():
    try:
        with open("indice.txt", "r", encoding="utf-8") as f:
            return int(f.read())
    except:
        return 0

def salvar_indice(i):
    with open("indice.txt", "w", encoding="utf-8") as f:
        f.write(str(i))

# ===== Geração inicial dos blocos a partir do livro.txt =====

def gerar_blocos(caminho):
    texto = ler_texto_completo(caminho)
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

# ===== Exibição do bloco atual =====

def mostrar_bloco_atual():
    blocos = ler_blocos()
    idx = ler_indice()

    if idx < 0 or idx >= len(blocos):
        print("Fim ou início do livro\n")
        return

    bloco_atual = blocos[idx]
    bloco_proximo = blocos[idx+1] if idx+1 < len(blocos) else ""
    salvar_bloco("atuais.txt", bloco_atual)
    salvar_bloco("proximos.txt", bloco_proximo)

    print("\n=== Bloco Atual ===")
    print(bloco_atual)

# ===== Avançar e retroceder =====

def avancar():
    blocos = ler_blocos()
    idx = ler_indice()
    if idx >= len(blocos) - 1:
        print("Acabou o livro")
        return
    salvar_indice(idx + 1)
    mostrar_bloco_atual()

def retroceder():
    idx = ler_indice()
    if idx == 0:
        print("Início do livro")
        return
    salvar_indice(idx - 1)
    mostrar_bloco_atual()

# ===== Execução principal =====

if not os.path.exists("blocos.txt"):
    gerar_blocos("livro.txt")

mostrar_bloco_atual()

while True:
    try:
        x = int(input("Digite 1 para retroceder, 2 para avançar: "))
        if x == 1:
            retroceder()
        elif x == 2:
            avancar()
        else:
            print("Opção inválida")
    except ValueError:
        print("Digite um número válido.")

