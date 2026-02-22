#Replicando meu genius em esp32
from machine import Pin
import random
from time import sleep

# ===== Variaveis-leds =====
ledRed = Pin(21, Pin.OUT)
ledBlue = Pin(19, Pin.OUT)
ledYellow = Pin(18, Pin.OUT)
ledGreen = Pin(5, Pin.OUT)

# ===== Variaveis-btn =====
btnRed = Pin(33, Pin.IN, Pin.PULL_UP)
btnBlue = Pin(4, Pin.IN, Pin.PULL_UP)
btnYellow = Pin(16, Pin.IN, Pin.PULL_UP)
btnGreen = Pin(17, Pin.IN, Pin.PULL_UP)

leds = [
    ledBlue,
    ledGreen,
    ledRed,
    ledYellow
]

sequencia = []

def randorizar(indice):
    sleep(0.4)
    leds[indice].on() #equivalente a value(1)
    sleep(0.6)
    leds[indice].off() #equivalente a value(0)

while True:
    indice = random.randint(0,3)
    sequencia.append(indice)
    print('Sequencia:',indice)
    for passo in sequencia:
        randorizar(passo)

#Link:https://wokwi.com/projects/456622149332864001