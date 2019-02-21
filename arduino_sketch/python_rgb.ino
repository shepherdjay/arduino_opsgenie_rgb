#include <Bridge.h>
#include <Process.h>
#include <Console.h>

int statusPin = 13;

int redPin = 3;
int greenPin = 6;
int bluePin = 11;

char pythonRed[4];
char pythonGreen[4];
char pythonBlue[4];

void runPython() {
  Process p;
  p.runShellCommand("python /mnt/sda1/pythonfiles/opsgeniergb/main.py");
}

void setup() {
  // Setup Bridge
  Bridge.begin(250000);

  // Setup memory space and pinouts:
  pinMode(redPin,OUTPUT);
  pinMode(greenPin,OUTPUT);
  pinMode(bluePin,OUTPUT);
  pinMode(statusPin,OUTPUT);
  memset(pythonRed, 0, 4);
  memset(pythonGreen, 0, 4);
  memset(pythonBlue, 0, 4);
}

void loop() {
  // Get the values:
  digitalWrite(statusPin, HIGH);
  runPython();
  digitalWrite(statusPin, LOW);
  Bridge.get("pythonRed",pythonRed,4);
  Bridge.get("pythonGreen",pythonGreen,4);
  Bridge.get("pythonBlue",pythonBlue,4);

  int redInt = atoi(pythonRed);
  int greenInt = atoi(pythonGreen);
  int blueInt = atoi(pythonBlue);
  setColor(redInt,greenInt,blueInt);
  delay(5000);
}

void setColor(int redValue, int greenValue, int blueValue) {
  analogWrite(redPin, redValue);
  analogWrite(greenPin, greenValue);
  analogWrite(bluePin, blueValue);
}
