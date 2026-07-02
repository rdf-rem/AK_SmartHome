//====================================
// Smart Home Projekt
// Version 1.6 -- Schritt 4: Sensordaten publishen
//====================================
#include <WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>
#include <ESP32Servo.h>

#define RED_LED     27
#define GREEN_LED   26
#define WHITE_LED   25
#define BUTTON_PIN  4
#define PIR_PIN     18
#define DHT_PIN     15
#define SERVO_PIN   19

#define DHT_TYPE DHT22

const char* WIFI_SSID = "Wokwi-GUEST";
const char* WIFI_PASS = "";

const char* MQTT_BROKER = "broker.hivemq.com";
const int   MQTT_PORT   = 1883;
const char* MQTT_CLIENT_ID = "esp32-ak_smarthome";

// Subscribe-Topics (ESP32 empfaengt Befehle)
const char* TOPIC_LIGHT  = "ak_smarthome/home/livingroom/light";
const char* TOPIC_BLINDS = "ak_smarthome/home/livingroom/blinds";

// Publish-Topics (ESP32 sendet Zustaende)
const char* TOPIC_TEMPERATURE = "ak_smarthome/home/kitchen/temperature";
const char* TOPIC_HUMIDITY    = "ak_smarthome/home/kitchen/humidity";
const char* TOPIC_PIR         = "ak_smarthome/home/bedroom/pir";
const char* TOPIC_BUTTON      = "ak_smarthome/home/button";

WiFiClient espClient;
PubSubClient mqttClient(espClient);

DHT dht(DHT_PIN, DHT_TYPE);
Servo blindsServo;

bool whiteState = false;
bool lastButton = HIGH;

unsigned long lastButtonPress = 0;
const unsigned long debounceDelay = 200;

bool redLedState = false;
unsigned long lastBlink = 0;
const unsigned long blinkInterval = 500;

bool servoOpen = false;
const int servoClosedAngle = 0;
const int servoOpenAngle   = 90;

unsigned long lastDhtRead = 0;
const unsigned long dhtInterval = 2000;

// letzter gesendeter PIR-Status, damit nicht bei jedem Loop-Durchlauf erneut published wird
bool lastMotionSent = false;

unsigned long lastReconnectAttempt = 0;
const unsigned long reconnectInterval = 5000;

void mqttCallback(char* topic, byte* payload, unsigned int length) {
  String message;
  for (unsigned int i = 0; i < length; i++) {
    message += (char)payload[i];
  }

  Serial.print("MQTT empfangen [");
  Serial.print(topic);
  Serial.print("]: ");
  Serial.println(message);

  if (String(topic) == TOPIC_LIGHT) {
    if (message == "ON") {
      whiteState = true;
      digitalWrite(WHITE_LED, HIGH);
    } else if (message == "OFF") {
      whiteState = false;
      digitalWrite(WHITE_LED, LOW);
    }
  }

  if (String(topic) == TOPIC_BLINDS) {
    if (message == "OPEN") {
      servoOpen = true;
      blindsServo.write(servoOpenAngle);
    } else if (message == "CLOSE") {
      servoOpen = false;
      blindsServo.write(servoClosedAngle);
    }
  }
}

void setupWifi() {
  Serial.print("Verbinde mit WLAN: ");
  Serial.println(WIFI_SSID);

  WiFi.begin(WIFI_SSID, WIFI_PASS);

  while (WiFi.status() != WL_CONNECTED) {
    delay(300);
    Serial.print(".");
  }

  Serial.println();
  Serial.print("WLAN verbunden! IP-Adresse: ");
  Serial.println(WiFi.localIP());
}

bool reconnectMqtt() {
  Serial.print("Verbinde mit MQTT-Broker...");

  if (mqttClient.connect(MQTT_CLIENT_ID)) {
    Serial.println(" verbunden!");
    mqttClient.subscribe(TOPIC_LIGHT);
    mqttClient.subscribe(TOPIC_BLINDS);
    Serial.println("Topics abonniert.");
    return true;
  } else {
    Serial.print(" fehlgeschlagen, rc=");
    Serial.println(mqttClient.state());
    return false;
  }
}

void setup() {
  Serial.begin(115200);

  pinMode(RED_LED, OUTPUT);
  pinMode(GREEN_LED, OUTPUT);
  pinMode(WHITE_LED, OUTPUT);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  pinMode(PIR_PIN, INPUT);

  digitalWrite(RED_LED, LOW);
  digitalWrite(GREEN_LED, HIGH);
  digitalWrite(WHITE_LED, LOW);

  dht.begin();

  blindsServo.attach(SERVO_PIN);
  blindsServo.write(servoClosedAngle);

  setupWifi();

  mqttClient.setServer(MQTT_BROKER, MQTT_PORT);
  mqttClient.setCallback(mqttCallback);
  reconnectMqtt();

  Serial.println("--------------------------------");
  Serial.println("Smart Home Version 1.6 gestartet");
  Serial.println("--------------------------------");
}

void loop() {
  if (!mqttClient.connected()) {
    if (millis() - lastReconnectAttempt > reconnectInterval) {
      lastReconnectAttempt = millis();
      reconnectMqtt();
    }
  } else {
    mqttClient.loop();
  }

  //============================
  // Taster (Weisse LED + Servo lokal, plus MQTT-Meldung)
  //============================
  bool button = digitalRead(BUTTON_PIN);
  if (button == LOW && lastButton == HIGH && (millis() - lastButtonPress) > debounceDelay) {
    lastButtonPress = millis();

    whiteState = !whiteState;
    digitalWrite(WHITE_LED, whiteState);

    servoOpen = !servoOpen;
    blindsServo.write(servoOpen ? servoOpenAngle : servoClosedAngle);

    Serial.print("Taster gedrueckt -> Licht: ");
    Serial.print(whiteState ? "AN" : "AUS");
    Serial.print(" | Rollo: ");
    Serial.println(servoOpen ? "OFFEN" : "GESCHLOSSEN");

    if (mqttClient.connected()) {
      mqttClient.publish(TOPIC_BUTTON, "PRESSED");
    }
  }
  lastButton = button;

  //============================
  // PIR
  //============================
  bool motion = digitalRead(PIR_PIN);
  if (motion) {
    digitalWrite(GREEN_LED, LOW);
    if (millis() - lastBlink >= blinkInterval) {
      lastBlink = millis();
      redLedState = !redLedState;
      digitalWrite(RED_LED, redLedState);
    }
  } else {
    digitalWrite(GREEN_LED, HIGH);
    digitalWrite(RED_LED, LOW);
    redLedState = false;
  }

  // PIR-Status nur bei Aenderung per MQTT senden (nicht bei jedem Loop-Durchlauf)
  if (motion != lastMotionSent) {
    lastMotionSent = motion;
    if (mqttClient.connected()) {
      mqttClient.publish(TOPIC_PIR, motion ? "MOTION" : "CLEAR");
      Serial.println(motion ? "MQTT gesendet: MOTION" : "MQTT gesendet: CLEAR");
    }
  }

  //============================
  // DHT22 (alle 2 Sekunden auslesen + publishen)
  //============================
  if (millis() - lastDhtRead >= dhtInterval) {
    lastDhtRead = millis();

    float temperature = dht.readTemperature();
    float humidity = dht.readHumidity();

    if (isnan(temperature) || isnan(humidity)) {
      Serial.println("DHT22: Fehler beim Auslesen!");
    } else {
      Serial.print("Temperatur: ");
      Serial.print(temperature);
      Serial.print(" C  |  Luftfeuchtigkeit: ");
      Serial.print(humidity);
      Serial.println(" %");

      if (mqttClient.connected()) {
        char tempString[8];
        dtostrf(temperature, 4, 2, tempString);
        mqttClient.publish(TOPIC_TEMPERATURE, tempString);

        char humString[8];
        dtostrf(humidity, 4, 2, humString);
        mqttClient.publish(TOPIC_HUMIDITY, humString);
      }
    }
  }
}
