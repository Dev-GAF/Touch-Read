import os

# Função para ler o texto completo do arquivo
def ler_texto_completo(caminho):
    with open(caminho, "r", encoding="utf-8") as f:
        return f.read()

def salvar_bloco(nome, conteudo):
    with open(nome, "w", encoding="utf-8") as f:
        f.write(conteudo)

def ler_bloco(nome):
    try:
        with open(nome, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""

def excluir_arquivos():
    try:
        os.remove("atuais.txt")
        os.remove("proximos.txt")
        os.remove("lidos.txt")
        print("Arquivos excluídos com sucesso!")
    except Exception as e:
        print(f"Erro ao excluir arquivos: {e}")

def avancar_bloco():

    caminho_original = "livro.txt"
    texto = ler_texto_completo(caminho_original)

    lidos = ler_bloco("lidos.txt")
    posicao_atual = len(lidos)

    restante = texto[posicao_atual:]

    if not restante:
        print("Acabou o livro\n")
        excluir_arquivos()
        return 0

    bloco_atual = ""
    i = 0

    while i < len(restante):
        palavra = ""
        while i < len(restante) and not restante[i].isspace():
            palavra += restante[i]
            i += 1

        espaco = ""
        while i < len(restante) and restante[i].isspace():
            espaco += restante[i]
            i += 1

        # Palavra inteira maior que 20, precisa ser quebrada
        if len(palavra) > 20:
            if bloco_atual == "":
                bloco_atual = palavra[:20]
                restante_novo = palavra[20:] + espaco + restante[i:]
            else:
                i -= len(palavra + espaco)
            break

        # Verifica se cabe no bloco
        if len(bloco_atual) + len(palavra) + len(espaco) <= 20:
            bloco_atual += palavra + espaco
        else:
            i -= len(palavra + espaco)
            break

    # Define novo conteúdo lido e restante
    novo_lidos = texto[:posicao_atual + len(bloco_atual)]
    restante_novo = texto[posicao_atual + len(bloco_atual):]

    bloco_proximo = restante_novo[:20]

    salvar_bloco("atuais.txt", bloco_atual)
    salvar_bloco("proximos.txt", bloco_proximo)
    salvar_bloco("lidos.txt", novo_lidos)

    print("\n=== Bloco Atual ===")
    print(bloco_atual)

    print()
    return 1, bloco_atual, novo_lidos, bloco_proximo

def retroceder_bloco():
    caminho_original = "livro.txt"
    texto = ler_texto_completo(caminho_original)
    lidos = ler_bloco("lidos.txt")

    if not lidos:
        print("Início do livro\n")
        return

    nova_posicao = max(0, len(lidos) - 20)
    novos_lidos = texto[:nova_posicao]
    bloco_atual = texto[nova_posicao:len(lidos)]
    bloco_proximo = texto[len(lidos):len(lidos) + 20]

    salvar_bloco("atuais.txt", bloco_atual)
    salvar_bloco("proximos.txt", bloco_proximo)
    salvar_bloco("lidos.txt", novos_lidos)

    print("\n=== Bloco Anterior ===")
    print(bloco_atual)


def simular_botao():
    input("Pressione Enter para avançar para o próximo bloco...")
    return avancar_bloco()

# Primeira execução
avancar_bloco()

# Loop contínuo
while True:
    x = int(input("Digite 1 para retroceder, 2 para avançar: "))

    if x == 1:
        retroceder_bloco()
    elif x == 2:
        if simular_botao() == 0:
            break
    else:
        print("Opção inválida")
