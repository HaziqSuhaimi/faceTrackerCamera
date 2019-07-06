#include <Servo.h>

Servo j1; // x axis
Servo j2; //y axis

int posX= 90;
int posY= 135;

bool state = true;
int xLim = 180;

void setup() {
  Serial.begin(115200);
  j1.attach(10);
  j2.attach(9);
  
  j1.write(posX);
  j2.write(posY);

}

void loop() {
  if(Serial.available() > 0) {
    char data = Serial.read();

     if (data == 'L'){
      posX += 1;
      j1.write(posX);
     }
     if (data == 'R'){
      posX -= 1;
      j1.write(posX);
     }
     if (data == 'C'){
      j1.write(posX);
     }
     if (data == 'A'){
      posY -= 1;
      j2.write(posY);
     }
     if (data == 'B'){
      posY += 1;
      j2.write(posY);
     }
     if (data == 'T'){
      j2.write(posY);
     } 
  }
}
// simple je an?? ngan aku xpayah susah2..
