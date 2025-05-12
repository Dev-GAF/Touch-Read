import sys
import os

# Adiciona a pasta raiz "Touch-Read" ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from arquivo import arq  

def alfabeto_em_numero():
    
    carac = arq.leitura_arquivo()
    
    numero = ord(carac.upper()) - ord('A') + 1
    
    return numero
