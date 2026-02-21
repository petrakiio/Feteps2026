#Comencando estudo no ESP32
#Site usado:https://wokwi.com/?utm_source=chatgpt.com
#EXtensão:https://docs.wokwi.com/vscode/getting-started
#link curso:https://youtu.be/P6qUlAc8KaU?si=CHYF1T8uZCPa0Kuf
#tutorial da extensão:https://youtu.be/35a4z4X2XZI?si=ZU_PzXMTmhnDFB18

#Codigo do video
from machine import Pin #Importando os pinos
from time import sleep #usado pro delay

ledRed = Pin(4, Pin.OUT) # Definindo o pino 4 como saida

while True:
  ledRed.value(1) #Liga o led: 1 > true
  sleep(2) # Espera 1 segundo
  ledRed.value(0) # Desliga o led: 0 > false
  sleep(2)

#Meu codigo