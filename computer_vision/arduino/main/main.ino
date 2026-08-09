#include <Servo.h>

int degrees_[5]; // Array que almacenará los grados de los servos
int current_degrees[5]; // Array para filtrear (evitar que la mano tambalee)
int aux = 10; // Auxiliar que ayuda a los servos a no tambalear
uint8_t pins_servos[5] = {8, 11, 6, 10, 9}; // pines pwm de los servos
Servo servos[5]; // Array que contiene los servos

void setup() {
  int i = 0;
  for (Servo &servo : servos){
    int pin = pins_servos[i];
    servo.attach(pin);
    i++;
  }
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() == 5) {// Si recibe datos por el serial
    for (int i = 0; i < 5; i++) {
      degrees_[i] = Serial.read();
    }
  }
  int i = 0;
  for (Servo &servo : servos){ // mueve los servos con sus respectivos grados
    if (abs(degrees_[i] - current_degrees[i]) > aux){
      servo.write(degrees_[i]);
      current_degrees[i] = degrees_[i];
    }
    i++;
  }
}
