from machine import Pin,I2C #importando a tela
import ssd1306 #biblioteca da tela oled

#Variaveis da tela 
i2c = I2C(0, scl=Pin(22), sda=Pin(21)) #Cria barramento
oled = ssd1306.SSD1306_I2C(128, 64, i2c) #Cria obj(objeto) da tela

#Controlando buttons
btn = Pin(19,Pin.IN,Pin.PULL_UP)
ledRed = Pin(16,Pin.OUT)

def escreverText():
    oled.fill(0)
    oled.text('Voce clicou!',0,0)
    oled.show()

def click():
    if btn.value() == 0:
        escreverText()
        ledRed.value(1)
    else:
        ledRed.value(0)

while True:
    click()
   