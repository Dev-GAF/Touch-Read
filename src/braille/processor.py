import time
from .mapping import BrailleMapping

class BrailleProcessor:
    def __init__(self):
        self.in_number_mode = False
        self.mapping = BrailleMapping()

    def is_in_caractere_map(self, carac):
        """
        Verifica se o caractere está presente no alfabeto (A–Z)
        """
        return carac.upper() in self.mapping.caracteres or carac in self.mapping.numeros

    def is_space(self, carac):
        return carac == " "

    def conversao_pinos(self, c: str):
        """
        Converte um caractere ou número para o formato de pinos Braille.
        O mapeamento é feito com base no alfabeto A-Z; 0-9.
        """
        if c.upper() in self.mapping.caracteres:
            return self.mapping.caracteres[c.upper()]
        elif c in self.mapping.numeros:
            letra = self.mapping.numeros[c]
            indicador_numeros = self.mapping.indicador_numeros["#"]
            return [indicador_numeros, self.mapping.caracteres[letra]]
        else:
            return [1, 1, 1, 1, 1, 1] 

    def mostrar_letra_por_letra(self, pinos_lista):
        """
        Exibe as letras em Braille, letra por letra.
        Para números, mostra o indicador uma única vez antes da sequência.
        """
        self.in_number_mode = False  

        for pinos in pinos_lista:
            if pinos == [1, 1, 1, 1, 1, 1]:
                self.in_number_mode = False  
                print("1 1 1 1 1 1", end="\r")
                time.sleep(2)
            elif isinstance(pinos, list) and len(pinos) == 2 and all(isinstance(p, list) for p in pinos):
                if not self.in_number_mode:
                    indicador = pinos[0]
                    print(" ".join(str(p) for p in indicador), end="\r")
                    time.sleep(1.5)

                    print("      ", end="\r")
                    time.sleep(0.5)

                    self.in_number_mode = True  
                numero = pinos[1]
                print(" ".join(str(p) for p in numero), end="\r")
                time.sleep(2)
            else:
                self.in_number_mode = False  
                print(" ".join(str(p) for p in pinos), end="\r")
                time.sleep(2)
        print() 

    def verificar_rep_palavra(self, palavraBraileana):
        """
        Repete a palavra novamente
        """
        repeticao = input()

        while repeticao == "rep":
            self.mostrar_letra_por_letra(palavraBraileana)
            repeticao = input()

    def processar_livro_por_palavra(self, caminho):
        """
        Processa o livro palavra por palavra e converte para Braille.
        Cada palavra é exibida na tela como um conjunto de pinos Braille.
        """
        try:
            indice = 1
            for palavra in caminho['textos']:
                print(f"\n=== Processando Palavra {indice}: '{palavra}' ===")

                numeros_lista = [self.conversao_pinos(c) for c in palavra]
                self.mostrar_letra_por_letra(numeros_lista)

                self.verificar_rep_palavra(numeros_lista)

                indice += 1
                time.sleep(1)  
        except Exception as e:
            print(f"Erro ao processar o livro: {e}")
