from machine import Pin
from time import sleep, ticks_ms, ticks_diff

# ------------------------------
# Configuração LEDs
# ------------------------------
led_pins = {
    1: Pin(5, Pin.OUT),
    2: Pin(4, Pin.OUT),
    3: Pin(2, Pin.OUT),
    4: Pin(19, Pin.OUT),
    5: Pin(16, Pin.OUT),
    6: Pin(18, Pin.OUT)
}

# ------------------------------
# Mapas Braille
# ------------------------------
braille_map = {
    "a": [1], "b": [1,2], "c": [1,4], "d": [1,4,5], "e": [1,5],
    "f": [1,2,4], "g": [1,2,4,5], "h": [1,2,5], "i": [2,4], "j": [2,4,5],
    "k": [1,3], "l": [1,2,3], "m": [1,3,4], "n": [1,3,4,5], "o": [1,3,5],
    "p": [1,2,3,4], "q": [1,2,3,4,5], "r": [1,2,3,5], "s": [2,3,4], "t": [2,3,4,5],
    "u": [1,3,6], "v": [1,2,3,6], "w": [2,4,5,6], "x": [1,3,4,6], "y": [1,3,4,5,6], "z": [1,3,5,6],
    ",": [2], ".": [2,5,6], ";": [2,3], ":": [2,5], "!": [2,3,5], "?": [2,6], "-": [3,6],
    " ": [],
    "1": [1], "2": [1,2], "3": [1,4], "4": [1,4,5], "5": [1,5],
    "6": [1,2,4], "7": [1,2,4,5], "8": [1,2,5], "9": [2,4], "0": [2,4,5]
}

signal_number = [3,4,5,6]  # ⠼
signal_capital = [6]       # ⠠

# ------------------------------
# Funções LEDs
# ------------------------------
def clear_leds():
    for pin in led_pins.values():
        pin.value(0)

# ------------------------------
# Botões
# ------------------------------
btn_back = Pin(32, Pin.IN, Pin.PULL_UP)
btn_pause = Pin(33, Pin.IN, Pin.PULL_UP)
btn_forward = Pin(25, Pin.IN, Pin.PULL_UP)

# ------------------------------
# Funções auxiliares
# ------------------------------
def find_prev_space(pos, antepenultimate=False):
    spaces = [i for i, c in enumerate(texto[:pos]) if c == " "]
    if antepenultimate and len(spaces) >= 2:
        return spaces[-2]
    elif spaces:
        return spaces[-1]
    return 0

def find_next_space(pos):
    for i in range(pos+1, len(texto)):
        if texto[i] == " ":
            return i
    return len(texto)-1

# ------------------------------
# Função não-bloqueante para mostrar letra
# ------------------------------
class BrailleDisplay:
    def __init__(self):
        self.letter = ""
        self.stages = []
        self.stage = 0
        self.start_time = 0
        self.duration = 1000  # 1 segundo por etapa

    def start(self, ch):
        self.letter = ch
        self.stage = 0
        self.start_time = ticks_ms()
        print("Mostrando letra:", ch)  # print no terminal
        # Definir etapas
        if ch.isdigit():
            self.stages = [signal_number, braille_map[ch]]
        elif ch.isalpha():
            if ch.isupper():
                self.stages = [signal_capital, braille_map[ch.lower()]]
            else:
                self.stages = [braille_map[ch]]
        elif ch == " ":
            self.stages = [[]]
        elif ch in braille_map:
            self.stages = [braille_map[ch]]
        else:
            print("Caractere não mapeado:", ch)
            self.stages = [[]]
        # Acender LEDs da primeira etapa
        clear_leds()
        for p in self.stages[0]:
            led_pins[p].value(1)

    def update(self):
        now = ticks_ms()
        if self.stage >= len(self.stages):
            clear_leds()
            return True  # letra terminou

        if ticks_diff(now, self.start_time) >= self.duration:
            # Passar para próxima etapa
            clear_leds()
            self.stage += 1
            self.start_time = now
            if self.stage < len(self.stages):
                for p in self.stages[self.stage]:
                    led_pins[p].value(1)
        return False  # ainda mostrando

# ------------------------------
# Loop principal
# ------------------------------
texto = "Ola Mundo 123!"
index = 0
paused = False
display = BrailleDisplay()
display.start(texto[index])

while index < len(texto):
    # Botões
    if not btn_back.value():
        # Volta para início da palavra anterior
        index = find_prev_space(find_prev_space(index)) + 1
        display.start(texto[index])
        sleep(0.3)  # debounce

    if not btn_pause.value():
        if paused:
            # Ao despausar, volta para início da palavra atual
            index = find_prev_space(index) + 1
            display.start(texto[index])
        paused = not paused
        sleep(0.3)  # debounce

    if not btn_forward.value():
        # Avança para início da próxima palavra
        index = find_next_space(index) + 1
        display.start(texto[index])
        sleep(0.3)  # debounce

    # Atualiza display apenas se não pausado
    if not paused:
        finished = display.update()
        if finished:
            index += 1
            if index < len(texto):
                display.start(texto[index])

