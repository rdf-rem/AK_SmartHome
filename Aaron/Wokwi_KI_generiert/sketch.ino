const int buttonPin = 2;
const int ledPin = 9;
const int ledPin2 = 10;
const int potPin = A0;

bool doorOpen = false;
int brightness = 0;

void setup() {
  pinMode(buttonPin, INPUT_PULLUP);
  pinMode(ledPin, OUTPUT);
  pinMode(ledPin2, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  int buttonState = digitalRead(buttonPin);
  brightness = analogRead(potPin) / 4;

  if (buttonState == LOW) {
    doorOpen = !doorOpen;
    delay(250);
  }

  if (doorOpen) {
    analogWrite(ledPin, brightness);
    digitalWrite(ledPin2, HIGH);
    Serial.println("Status: Tür offen");
  } else {
    analogWrite(ledPin, 0);
    digitalWrite(ledPin2, LOW);
    Serial.println("Status: Tür geschlossen");
  }

  delay(100);
}
