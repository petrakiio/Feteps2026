#codigo pra rodar

from machine import Pin
from time import sleep

led_red = Pin(25, Pin.OUT)
led_yellow = Pin(26, Pin.OUT)
led_green = Pin(27, Pin.OUT)


def all_off():
    led_red.value(0)
    led_yellow.value(0)
    led_green.value(0)


def run_cycle():
    all_off()
    led_red.value(1)
    sleep(3)

    all_off()
    led_yellow.value(1)
    sleep(1)

    all_off()
    led_green.value(1)
    sleep(3)

    all_off()
    led_yellow.value(1)
    sleep(1)


while True:
    run_cycle()
