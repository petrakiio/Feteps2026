#Meu codigo de semaforo

from machine import Pin #Importando os pinos
from time import sleep #usado pro delay

#Definindo pinos
ledRed = Pin(4, Pin.OUT) 
ledYellow = Pin(0, Pin.OUT)
ledGreen = Pin(2, Pin.OUT)

def timer(t=2):
    sleep(t)

def all_off():
    ledRed.value(0)
    ledYellow.value(0)
    ledGreen.value(0)

def main():
    # Vermelho
    all_off()
    ledRed.value(1)
    timer(3)

    # Amarelo (transição)
    all_off()
    ledYellow.value(1)
    timer(1)

    # Verde
    all_off()
    ledGreen.value(1)
    timer(3)

    # Amarelo (antes de fechar)
    all_off()
    ledYellow.value(1)
    timer(1)

while True:
    main()