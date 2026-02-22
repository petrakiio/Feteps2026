## Rodar o semaforo no ESP32 (MicroPython)

### 1) Ligacao dos LEDs
Use 1 resistor de 220R para cada LED.

- LED vermelho: GPIO25 -> resistor -> anodo do LED, catodo -> GND
- LED amarelo: GPIO26 -> resistor -> anodo do LED, catodo -> GND
- LED verde: GPIO27 -> resistor -> anodo do LED, catodo -> GND

### 2) Instalar firmware MicroPython no ESP32 (uma vez)
Baixe o firmware ESP32 em:
https://micropython.org/download/ESP32_GENERIC/

Grave no chip:

```bash
esptool.py --chip esp32 --port /dev/ttyUSB0 erase_flash
esptool.py --chip esp32 --port /dev/ttyUSB0 --baud 460800 write_flash -z 0x1000 ESP32_GENERIC-*.bin
```

Se sua porta for diferente, troque `/dev/ttyUSB0`.

### 3) Enviar seu codigo para a placa
Renomeie `Estudos/sem.py` para `main.py` no ESP32.

Com `mpremote`:

```bash
mpremote connect /dev/ttyUSB0 fs cp Estudos/sem.py :main.py
mpremote connect /dev/ttyUSB0 reset
```

### 4) Teste
Ao reiniciar a placa, o ciclo deve ficar:
vermelho (3s) -> amarelo (1s) -> verde (3s) -> amarelo (1s).

## Observacao sobre `wokmwi.toml`
Esse arquivo e para simulacao/build no Wokwi VS Code (mais comum em C/C++).
Para ESP32 real com MicroPython, o essencial e firmware + `main.py` na placa.
