def leitura_arquivo():
    
    with open('testes/teste01.txt', 'r', encoding='utf-8') as arq:
        return arq.read(1)

