#include <WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>
#include <Servo.h>

// Update these values for your Wokwi / ESP32 simulation environment
const char* ssid = "Wokwi-GUEST";
const char* password = "";
const char* mqtt_server = "broker.hivemq.com";
const int mqtt_port = 1883;

const int LED_PIN = 2;
const int DHTPIN = 4;
const int PIR_PIN = 13;
const int SERVO_PIN = 5;

const char* topic_gesture = "home/gesture";
const char* topic_light = "home/livingroom/light";
const char* topic_blinds = "home/livingroom/blinds";
const char* topic_temperature = "home/kitchen/temperature";
const char* topic_pir = "home/bedroom/pir";
const char* topic_button = "home/button";

WiFiClient espClient;
PubSubClient client(espClient);
DHT dht(DHTPIN, DHT22);
Servo blindsServo;

bool lightState = false;
int blindsAngle = 0;
unsigned long lastSensorPublish = 0;

void callback(char* topic, byte* payload, unsigned int length) {
  String message;
  for (unsigned int i = 0; i < length; i++) {
    message += (char)payload[i];
  }

  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  Serial.println(message);

  if (String(topic) == topic_light) {
    if (message == "ON") {
      digitalWrite(LED_PIN, HIGH);
      lightState = true;
    } else if (message == "OFF") {
      digitalWrite(LED_PIN, LOW);
      lightState = false;
    }
  }

  if (String(topic) == topic_blinds) {
    if (message == "OPEN") {
      blindsAngle = 0;
      blindsServo.write(blindsAngle);
    } else if (message == "CLOSED") {
      blindsAngle = 90;
      blindsServo.write(blindsAngle);
    }
  }
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("ESP32SmartHomeSubscriber")) {
      Serial.println("connected");
      client.subscribe(topic_light);
      client.subscribe(topic_blinds);
      client.subscribe(topic_gesture);
      client.subscribe(topic_button);
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  delay(1000);

  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);

  pinMode(PIR_PIN, INPUT);
  dht.begin();
  blindsServo.attach(SERVO_PIN);
  blindsServo.write(blindsAngle);

  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print('.');
  }
  Serial.println();
  Serial.print("WiFi connected, IP: ");
  Serial.println(WiFi.localIP());

  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(callback);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  unsigned long now = millis();
  if (now - lastSensorPublish > 10000) {
    lastSensorPublish = now;

    float temperature = dht.readTemperature();
    bool pirDetected = digitalRead(PIR_PIN) == HIGH;

    if (!isnan(temperature)) {
      String tempString = String(temperature, 1);
      client.publish(topic_temperature, tempString.c_str());
    }

    client.publish(topic_pir, pirDetected ? "1" : "0");
    client.publish(topic_gesture, lightState ? "light_on" : "light_off");
  }
}
