from mapeamento import map_carac as mp

def is_in_caractere_map(carac):
    """
    Verifica se o caractere está presente no alfabeto (A–Z)
    """

    return carac.upper() in mp.caracteres or carac in mp.numeros

def is_space(carac):
    return carac == " "

def conversao_pinos(c: str):
    """
    Converte um caractere ou número para o formato de pinos Braille.
    O mapeamento é feito com base no alfabeto A-Z; 0-9.
    """ 
    if c.upper() in mp.caracteres:
        return mp.caracteres[c.upper()]
    elif c in mp.numeros:
        letra = mp.numeros[c]
        return mp.caracteres[letra]
    else:
        return [1, 1, 1, 1, 1, 1]  # caractere inválido ou espaço