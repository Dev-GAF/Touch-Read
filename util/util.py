import mapeamento as mp

def is_esta(c):
    """
    Verifica se o caractere é válido para Braille (alfabeto A-Z ou espaço).
    """
    return c.isalpha() or c.isspace()


def conversao_pinos(c: str, type: str):
    """
    Converte um caractere ou número para o formato de pinos Braille.
    O mapeamento é feito com base no alfabeto A-Z; 0-9.
    """
    
    if type=="caracteres":
        pinos = mp.caracteres.get(c)
        if pinos:
            return pinos
            
    if type=="numeros":
        letra = mp.numeros.get(c)
        if letra:
            return mp.caracteres.get(letra)
        
    return [1, 1, 1, 1, 1, 1]