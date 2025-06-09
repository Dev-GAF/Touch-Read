def ler_texto_completo(caminho):
    with open(caminho, "r", encoding="utf-8") as f:
        return f.read()

def salvar_texto(caminho, conteudo):
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(conteudo)

# def ler_texto_completo(caminho):
#     with open(caminho, "r", encoding="utf-8") as f:
#         return f.read()

# def salvar_bloco(nome, conteudo):
#     with open(nome, "w", encoding="utf-8") as f:
#         f.write(conteudo)

# def ler_blocos():
#     with open("blocos.txt", "r", encoding="utf-8") as f:
#         return f.read().splitlines()

# def ler_indice():
#     try:
#         with open("indice.txt", "r", encoding="utf-8") as f:
#             return int(f.read())
#     except:
#         return 0

# def salvar_indice(i):
#     with open("indice.txt", "w", encoding="utf-8") as f:
#         f.write(str(i))