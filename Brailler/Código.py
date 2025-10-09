from machine import Pin
from time import sleep, ticks_ms, ticks_diff
import network
import urequests
import ujson
import time

# ------------------------------
# Configuração LEDs
# ------------------------------
led_pins = {
    1: Pin(5, Pin.OUT),
    2: Pin(4, Pin.OUT),
    3: Pin(2, Pin.OUT),
    4: Pin(19, Pin.OUT),
    5: Pin(21, Pin.OUT),
    6: Pin(18, Pin.OUT)
}

# ------------------------------
# Mapas Braille
# ------------------------------
braille_map = {
    "a": [2,3,4,5,6], "b": [3,4,5,6], "c": [2,3,5,6], "d": [2,3,6], "e": [2,3,4,6],
    "f": [3,5,6], "g": [3,6], "h": [3,4,6], "i": [1,3,5,6], "j": [1,3,6],
    "k": [2,4,5,6], "l": [4,5,6], "m": [2,5,6], "n": [2,6], "o": [2,4,6],
    "p": [5,6], "q": [6], "r": [4,6], "s": [1,5,6], "t": [1,6],
    "u": [2,4,5], "v": [5], "w": [1,3], "x": [2,5], "y": [2], "z": [2,4],
    ",": [1,3,4,5,6], ".": [1,3,4], ";": [1,4,5,6], ":": [1,3,4,6], "!": [1,4,6],
    "?": [1,2,3,4,5], "-": [1,2,4,5],
    " ": [1,2,3,4,5,6],
    "1": [2,3,4,5,6], "2": [3,4,5,6], "3": [2,3,5,6], "4": [2,3,6], "5": [2,3,4,6],
    "6": [3,5,6], "7": [3,6], "8": [3,4,6], "9": [1,3,5,6], "0": [1,3,6]
}

signal_number = [1,2]  # ⠼
signal_capital = [1,2,3,4,5]       # ⠠

# ------------------------------
# Funções LEDs
# ------------------------------
def clear_leds():
    for pin in led_pins.values():
        pin.value(0)

def acende_leds(pinos):
    clear_leds()
    for p in pinos:
        led_pins[p].value(1)
    print("LEDs acesos nos pinos:", pinos)

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
        print("\nMostrando letra:", ch)
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

        if self.stages:
            acende_leds(self.stages[0])

    def update(self):
        now = ticks_ms()
        if self.stage >= len(self.stages):
            clear_leds()
            return True  # letra terminou

        if ticks_diff(now, self.start_time) >= self.duration:
            self.stage += 1
            self.start_time = now
            if self.stage < len(self.stages):
                acende_leds(self.stages[self.stage])
        return False  # ainda mostrando

# ------------------------------
# Wi-Fi e API
# ------------------------------
SSID = "J"
PASSWORD = "12345678"

def conecta_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Conectando ao Wi-Fi...")
        wlan.connect(SSID, PASSWORD)
        while not wlan.isconnected():
            time.sleep(0.5)
    print("Conectado! IP:", wlan.ifconfig()[0])

def pega_texto_da_api(livro_id=111, pagina=0):
    while True:
        url = f"https://livrostr.onrender.com/livro/{livro_id}"
        if pagina > 0:
            url += f"/{pagina}"
        print("Buscando:", url)
        try:
            resp = urequests.get(url)
            data = ujson.loads(resp.text)
            resp.close()
            
            texto_final = ""
            for livro in data.values():
                for item in livro:
                    texto_final += item.get("Trecho", "") + " "
            texto_final = texto_final.strip()
            
            if texto_final:
                return texto_final
            else:
                pagina += 1
        except Exception as e:
            print("Erro ao acessar API:", e)
            return "Erro ao acessar API"

# ------------------------------
# Loop principal
# ------------------------------
def main():
    global texto
    conecta_wifi()
    pagina_atual = 0
    texto = pega_texto_da_api(pagina=pagina_atual)
    
    index = 0
    paused = False
    display = BrailleDisplay()
    display.start(texto[index])

    while True:
        # Botões
        if not btn_back.value():
            index = find_prev_space(find_prev_space(index)) + 1
            display.start(texto[index])
            sleep(0.3)

        if not btn_pause.value():
            if paused:
                index = find_prev_space(index) + 1
                display.start(texto[index])
            paused = not paused
            sleep(0.3)

        if not btn_forward.value():
            index = find_next_space(index) + 1
            display.start(texto[index])
            sleep(0.3)

        # Atualiza display apenas se não pausado
        if not paused:
            finished = display.update()
            if finished:
                index += 1
                if index >= len(texto):
                    pagina_atual += 1
                    texto = pega_texto_da_api(pagina=pagina_atual)
                    index = 0
                if index < len(texto):
                    display.start(texto[index])

main()
