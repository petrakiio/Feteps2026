#include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

const char* ssid = "SEU_WIFI";
const char* password = "SENHA";

unsigned long tempoAnterior = 0;
const long intervalo = 60000;

void setup() {
    Serial.begin(115200);

    WiFi.begin(ssid, password);

    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
    }
}

void loop() {
    unsigned long agora = millis();

    if (agora - tempoAnterior >= intervalo) {
        tempoAnterior = agora;

        if (WiFi.status() == WL_CONNECTED) {
            HTTPClient http;

            http.begin("http://127.0.0.1:8000/api/alert/");

            int httpCode = http.GET();

            if (httpCode > 0) {
                String payload = http.getString();

                Serial.println(payload);

                DynamicJsonDocument doc(1024);
                deserializeJson(doc, payload);

                bool liberar = doc["ok"];

                if (liberar) {
                    Serial.println("💊 Liberar remédio!");

                    // aqui chama o motor
                    // girarMotor();
                }
            }

            http.end();
        }
    }
}