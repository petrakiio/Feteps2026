from machine import Pin

#Controlando buttons
btn = Pin(19,Pin.IN,Pin.PULL_UP)
ledRed = Pin(16,Pin.OUT)

#Em desenvolvimento
while True:
    if btn.value() == 0:
        ledRed.value(1)
    else:
        ledRed.value(0)