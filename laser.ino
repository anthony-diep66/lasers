#include <Servo.h>
#define DELAY 15
Servo sx, sy;
String serialData;
const int sxpn1 = 10, sypn2 = 11;
String packet;
void setup() {
  // put your setup code here, to run once:
  sx.attach(sxpn1);
  sy.attach(sypn2);
  Serial.begin(9600);
  Serial.setTimeout(10);
}


void loop() {
  
  serialData = Serial.readString();
  sx.write(parseDataX(serialData));
  sy.write(parseDataY(serialData));
}


int parseDataX(String data) {
  while( Serial.available() == 0 ) { }

  data.remove(data.indexOf("Y"));
  data.remove(data.indexOf("X"), 1);
  return data.toInt();
}

int parseDataY(String data) {
  data.remove(0, data.indexOf("Y") + 1);
  return data.toInt();
}
