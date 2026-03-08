#include <Stepper.h>

// Número de passos por volta do 28BYJ-48 com redutor (~2048)
const int stepsPerRevolution = 2048;

// Pinos conectados ao IN1 a IN4 do driver ULN2003
Stepper myStepper(stepsPerRevolution, 8, 10, 9, 11);

void setup() {
  myStepper.setSpeed(10); // Velocidade em RPM
  Serial.begin(9600);
}

void loop() {
  Serial.println("Girando sentido horário");
  myStepper.step(stepsPerRevolution); // Uma volta
  delay(1000);

  Serial.println("Girando sentido anti-horário");
  myStepper.step(-stepsPerRevolution); // Volta inversa
  delay(1000);
}