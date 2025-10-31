from machine import Pin, PWM
from time import sleep, ticks_ms, ticks_diff
import network
import urequests
import ujson
import time
import os

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
    "a": [2, 3, 4, 5, 6],
    "b": [3, 4, 5, 6],
    "c": [2, 3, 5, 6],
    "d": [2, 3, 6],
    "e": [2, 3, 4, 6],
    "f": [3, 5, 6],
    "g": [3, 6],
    "h": [3, 4, 6],
    "i": [1, 3, 5, 6],
    "j": [1, 3, 6],
    "k": [2, 4, 5, 6],
    "l": [4, 5, 6],
    "m": [2, 5, 6],
    "n": [2, 6],
    "o": [2, 4, 6],
    "p": [5, 6],
    "q": [6],
    "r": [4, 6],
    "s": [1, 5, 6],
    "t": [1, 6],
    "u": [2, 4, 5],
    "v": [5],
    "w": [1, 3],
    "x": [2, 5],
    "y": [2],
    "z": [2, 4],
    "á": [3, 4, 5],
    "à": [3, 4, 5],
    "â": [3, 4, 5],
    "ã": [2, 4, 5],
    "é": [2, 3, 4],
    "ê": [2, 3, 4],
    "í": [1, 3, 5],
    "ó": [2, 4],
    "ô": [2, 4],
    "õ": [2, 4, 5],
    "ú": [2, 4, 5],
    "ç": [4, 5],
    ".": [1, 3, 4],
    ",": [1, 3, 4, 5, 6],
    ";": [1, 6],
    ":": [1, 2, 3, 5],
    "?": [1, 3, 4, 5],
    "!": [1, 4],
    "-": [1, 2, 4, 5],
    "(": [1, 4],
    ")": [1, 4],
    "1": [2, 3, 4, 5, 6],
    "2": [3, 4, 5, 6],
    "3": [2, 3, 5, 6],
    "4": [2, 3, 6],
    "5": [2, 3, 4, 6],
    "6": [3, 5, 6],
    "7": [3, 6],
    "8": [3, 4, 6],
    "9": [1, 3, 5, 6],
    "0": [1, 3, 6],
    " ": []
}

signal_number = [1, 2]         # ⠼
signal_capital = [1, 2, 3, 4, 5]  # ⠠

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
# Funções de progresso
# ------------------------------
PROGRESS_FILE = "progresso.txt"

def salvar_progresso(pagina, index):
    try:
        with open(PROGRESS_FILE, "w") as f:
            f.write(f"{pagina},{index}")
        print(f"Progresso salvo: página {pagina}, índice {index}")
    except Exception as e:
        print("Erro ao salvar progresso:", e)

def apagar_progresso():
    try:
        if PROGRESS_FILE in os.listdir():
            os.remove(PROGRESS_FILE)
            print("Arquivo de progresso apagado.")
    except Exception as e:
        print("Erro ao apagar progresso:", e)

def carregar_progresso():
    try:
        if PROGRESS_FILE in os.listdir():
            with open(PROGRESS_FILE, "r") as f:
                content = f.read().strip()
                if content:
                    pagina, index = map(int, content.split(","))
                    print(f"Progresso carregado: página {pagina}, índice {index}")
                    return pagina, index
    except Exception:
        pass
    return 0, 0  # início padrão

# ------------------------------
# Funções auxiliares
# ------------------------------
def find_prev_space(pos):
    spaces = [i for i, c in enumerate(texto[:pos]) if c == " "]
    if spaces:
        return spaces[-1]
    return 0

def find_next_space(pos):
    for i in range(pos + 1, len(texto)):
        if texto[i] == " ":
            return i
    return len(texto) - 1

# ------------------------------
# Classe de exibição Braille
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
            self.stages = [[]]

        if self.stages:
            acende_leds(self.stages[0])

    def update(self):
        now = ticks_ms()
        if self.stage >= len(self.stages):
            clear_leds()
            return True
        if ticks_diff(now, self.start_time) >= self.duration:
            self.stage += 1
            self.start_time = now
            if self.stage < len(self.stages):
                acende_leds(self.stages[self.stage])
        return False

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

    # Beep de confirmação
    buzzer = PWM(Pin(13))
    buzzer.freq(1000)
    buzzer.duty(512)
    sleep(0.5)
    buzzer.duty(0)
    buzzer.deinit()

def pega_texto_da_api(livro_id=6, pagina=0):
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

        except Exception:
            buzzer = PWM(Pin(13))
            buzzer.freq(1000)
            for _ in range(2):
                buzzer.duty(512)
                sleep(0.3)
                buzzer.duty(0)
                sleep(0.2)
            buzzer.deinit()
            return "Fim"

# ------------------------------
# Loop principal
# ------------------------------
def main():
    global texto
    conecta_wifi()

    pagina_atual, index = carregar_progresso()
    texto = pega_texto_da_api(pagina=pagina_atual)
    display = BrailleDisplay()
    display.start(texto[index])
    paused = False

    while True:
        if not btn_back.value():
            prev_space = find_prev_space(index)
            if prev_space == 0 and pagina_atual > 0:
                pagina_atual -= 1
                texto = pega_texto_da_api(pagina=pagina_atual)
                index = len(texto) - 1
            else:
                index = prev_space
            display.start(texto[index])
            salvar_progresso(pagina_atual, index)
            sleep(0.3)

        if not btn_pause.value():
            if paused:
                index = find_prev_space(index) + 1
                display.start(texto[index])
            paused = not paused
            sleep(0.3)

        if not btn_forward.value():
            sleep(0.2)
            second_click = False
            start_wait = ticks_ms()
            while ticks_diff(ticks_ms(), start_wait) < 400:
                if not btn_forward.value():
                    second_click = True
                    sleep(0.2)
                    break

            if second_click:
                next_space = find_next_space(index)
                if next_space < len(texto) - 1:
                    index = next_space + 1
                    display.start(texto[index])
                    salvar_progresso(pagina_atual, index)
                else:
                    pagina_atual += 1
                    novo_texto = pega_texto_da_api(pagina=pagina_atual)
                    if novo_texto:
                        texto = novo_texto
                        index = 0
                        display.start(texto[index])
                        apagar_progresso()  # apaga arquivo ao mudar de trecho
                    else:
                        buzzer = PWM(Pin(13))
                        buzzer.freq(1000)
                        for _ in range(2):
                            buzzer.duty(512)
                            sleep(0.3)
                            buzzer.duty(0)
                            sleep(0.2)
                        buzzer.deinit()
            else:
                prev_space = find_prev_space(index)
                index = prev_space
                display.start(texto[index])
                salvar_progresso(pagina_atual, index)
            sleep(0.3)

        if not paused:
            finished = display.update()
            if finished:
                index += 1
                if index >= len(texto):
                    pagina_atual += 1
                    texto = pega_texto_da_api(pagina=pagina_atual)
                    index = 0
                    apagar_progresso()  # apaga ao mudar de trecho
                if index < len(texto):
                    display.start(texto[index])
                    salvar_progresso(pagina_atual, index)

# ------------------------------
# Execução
# ------------------------------
main()

