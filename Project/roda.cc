#include <Stepper.h>

// Número de passos por volta do motor 28BYJ-48 (~2048)
const int stepsPerRevolution = 2048;

// Pinos conectados ao driver ULN2003 (IN1, IN2, IN3, IN4)
Stepper myStepper(stepsPerRevolution, 8, 10, 9, 11);

void setup() {
  // Define velocidade do motor (RPM)
  myStepper.setSpeed(10);

  // Inicia comunicação serial
  Serial.begin(9600);
}

void loop() {

  // Gira no sentido horário
  Serial.println("Girando sentido horario");
  myStepper.step(stepsPerRevolution);
  delay(1000);

  // Gira no sentido anti-horário
  Serial.println("Girando sentido anti-horario");
  myStepper.step(-stepsPerRevolution);
  delay(1000);

}