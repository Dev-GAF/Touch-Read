import time
import json
import os
from .mapping import BrailleMapping

class BrailleProcessor:

    def __init__(self):
        self.in_number_mode = False
        self.mapping = BrailleMapping()
        self.progresso_file = "progresso.json" 

    def _salvar_progresso(self, paragrafo_idx, palavra_idx):
        """
        Salva o progresso atual em um arquivo JSON.
        """
        
        progresso = {
            "paragrafo_idx": paragrafo_idx,
            "palavra_idx": palavra_idx
        }
        with open(self.progresso_file, 'w') as f:
            json.dump(progresso, f)

    def _carregar_progresso(self):
        """
        Carrega o progresso de um arquivo JSON, se existir.
        """

        if os.path.exists(self.progresso_file):
            try:
                with open(self.progresso_file, 'r') as f:
                    progresso = json.load(f)
                    return progresso.get("paragrafo_idx", 0), progresso.get("palavra_idx", 0)
            except (json.JSONDecodeError, IOError):
                return 0, 0
            
        return 0, 0

    def _limpar_progresso(self):
        """
            Remove o arquivo de progresso ao concluir a leitura.
        """
        
        if os.path.exists(self.progresso_file):
            os.remove(self.progresso_file)

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

    def separar_texto_em_palavras(self, texto):
        palavras = texto.split()
        return palavras

    def mostrar_letra_por_letra(self, pinos_lista, palavra_atual=""):
        """
        Exibe a animação letra por letra e, ao final, deixa a representação
        Braille completa da palavra impressa na tela.
        """
        self.in_number_mode = False
        
        print(f"Palavra: {palavra_atual}                ", end="\r")
        time.sleep(1)

        for pinos in pinos_lista:
            print(" " * (len(palavra_atual) + 20), end="\r")

            if pinos == [1, 1, 1, 1, 1, 1]:
                self.in_number_mode = False
                print("1 1 1 1 1 1", end="\r")
                time.sleep(1)
            elif isinstance(pinos, list) and len(pinos) == 2 and all(isinstance(p, list) for p in pinos):
                if not self.in_number_mode:
                    indicador = pinos[0]
                    print(" ".join(str(p) for p in indicador), end="\r")
                    time.sleep(1)
                    print("      ", end="\r")
                    time.sleep(0.5)
                    self.in_number_mode = True
                numero = pinos[1]
                print(" ".join(str(p) for p in numero), end="\r")
                time.sleep(1)
            else:
                self.in_number_mode = False
                print(" ".join(str(p) for p in pinos), end="\r")
                time.sleep(1)

        braille_chars_formatados = []
        for item in pinos_lista:
            if isinstance(item, list) and len(item) == 2 and all(isinstance(p, list) for p in item):
                indicador_str = " ".join(map(str, item[0]))
                char_str = " ".join(map(str, item[1]))
                braille_chars_formatados.append(f"{indicador_str}  {char_str}")
            else:
                braille_chars_formatados.append(" ".join(map(str, item)))
        
        string_final = "  ".join(braille_chars_formatados)

        print(" " * (len(palavra_atual) + 20), end="\r")
        print(f"Braille: {string_final}")

    def solicitar_repeticao_palavra(self, pinos_lista, palavra_atual):
        """
        Pausa após uma palavra. Se o input for 'r', repete a palavra.
        O usuário deve pressionar Enter para continuar para a próxima palavra.
        """

        try:
            comando = input()

            while comando.lower().strip() == 'r':

                self.mostrar_letra_por_letra(pinos_lista, palavra_atual)

                comando = input()

        except EOFError:
            pass

    def solicitar_repeticao_paragrafo(self, paragrafo_em_braille):
        """
        Aguarda o input do usuário. Se for 'rep', repete a leitura do parágrafo inteiro.
        Esta função atua como um ponto de pausa, esperando a ação do usuário.
        """
        try:

            comando = input()
            
            while comando.lower().strip() == "rep":

                self.mostrar_letra_por_letra(paragrafo_em_braille)

                comando = input()
                
        except EOFError:
            pass

    def processar_livro_por_palavra(self, caminho):
        """
        Processa o livro permitindo repetição de palavra e de parágrafo.
        O progresso é salvo apenas ao final de cada parágrafo.
        """
        try:
            inicio_paragrafo, _ = self._carregar_progresso()

            if inicio_paragrafo > 0:
                print(f"\n--- Resumindo a partir do parágrafo {inicio_paragrafo + 1} ---")

            for indice, paragrafo in enumerate(caminho['textos']):

                if indice < inicio_paragrafo:
                    continue

                print("\n" + "="*40)

                print(f"Lendo parágrafo {indice + 1}:")

                print(paragrafo)

                print("="*40 + "\n")

                time.sleep(2)

                lista_de_palavras = self.separar_texto_em_palavras(paragrafo)

                paragrafo_em_braille_completo = []

                for palavra in lista_de_palavras:
                    numeros_lista = [self.conversao_pinos(c) for c in palavra]
                    
                    if paragrafo_em_braille_completo:
                        paragrafo_em_braille_completo.append([1, 1, 1, 1, 1, 1])

                    paragrafo_em_braille_completo.extend(numeros_lista)

                    self.mostrar_letra_por_letra(numeros_lista, palavra)
                    self.solicitar_repeticao_palavra(numeros_lista, palavra)
                
                self.solicitar_repeticao_paragrafo(paragrafo_em_braille_completo)
                self._salvar_progresso(indice + 1, 0)

            print("\n--- Leitura concluída com sucesso! O progresso foi zerado. ---")
            self._limpar_progresso()

        except KeyboardInterrupt:

            print("\n\nPrograma interrompido. Seu progresso foi salvo.")

        except Exception as e:

            print(f"Erro ao processar o livro: {e}. Seu progresso pode ter sido salvo.")