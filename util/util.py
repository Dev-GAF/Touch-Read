import mapeamento as mp

def is_in_caractere_map(carac):
    """
    Verifica se o caractere está presente no alfabeto (A–Z)
    """
    
    return carac.upper() in mp.caracteres

def is_in_numeros_map(num):
    """
    Verifica se o número está presente nos números de (0–9)
    """
    return num in mp.numeros
    

def conversao_pinos(x: str):
    """
    Converte um caractere ou número para o formato de pinos Braille.
    O mapeamento é feito com base no alfabeto A-Z; 0-9.
    """
    
    if is_in_caractere_map(x):
        pinos = mp.caracteres.get(x)
        if pinos:
            return pinos
    
    numero = [mp.indicador_numeros.get("#")]
    if is_in_numeros_map(x):
        letra = mp.numeros.get(x)
        if letra:
            numero.append(mp.caracteres.get(letra))
            return numero
        
    return [1, 1, 1, 1, 1, 1]