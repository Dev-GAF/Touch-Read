def is_esta(c):
    """
    Verifica se o caractere é válido para Braille (alfabeto A-Z ou espaço).
    """
    return c.isalpha() or c.isspace()


def conversao_pinos(c):
    """
    Converte um caractere para o formato de pinos Braille.
    O mapeamento é feito com base no alfabeto A-Z.
    """
    caracteres = {
        "A": [0, 1, 1, 1, 1, 1],
        "B": [0, 1, 0, 1, 1, 1],
        "C": [0, 0, 1, 1, 1, 1],
        "D": [0, 0, 1, 0, 1, 1],
        "E": [0, 1, 1, 0, 1, 1],
        "F": [0, 0, 0, 1, 1, 1],
        "G": [0, 0, 0, 0, 1, 1],
        "H": [0, 1, 0, 0, 1, 1],
        "I": [1, 0, 0, 1, 1, 1],
        "J": [1, 0, 0, 0, 1, 1],
        "K": [0, 1, 1, 1, 0, 1],
        "L": [0, 1, 0, 1, 0, 1],
        "M": [0, 0, 1, 1, 0, 1],
        "N": [0, 0, 1, 0, 0, 1],
        "O": [0, 1, 1, 0, 0, 1],
        "P": [0, 0, 0, 1, 0, 1],
        "Q": [0, 0, 0, 0, 0, 1],
        "R": [0, 1, 0, 0, 0, 1],
        "S": [1, 0, 0, 1, 0, 1],
        "T": [1, 0, 0, 0, 0, 1],
        "U": [0, 1, 1, 1, 0, 0],
        "V": [0, 1, 0, 1, 0, 0],
        "W": [1, 0, 0, 0, 1, 0],
        "X": [0, 0, 1, 1, 0, 0],
        "Y": [0, 0, 1, 0, 0, 0],
        "Z": [0, 1, 1, 0, 0, 0]
    }

    idx = ord(c.upper()) - 65  # Converte o caractere para o índice (A = 0, B = 1, ...)
    if 0 <= idx < 26:
        return caracteres[chr(idx + 65)]  # Retorna os pinos para a letra correspondente
    return [0, 0, 0, 0, 0, 0]  # Caso o caractere não seja reconhecido, retorna zeros (espaço)
