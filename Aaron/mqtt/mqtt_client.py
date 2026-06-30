"""
mqtt_client.py

Verwaltet die Verbindung zum MQTT-Broker.

Autor: Aaron
Unterstützung: ChatGPT
Projekt: Smart Home Steuerung mittels Gestenerkennung
"""

import paho.mqtt.client as mqtt


class MQTTClient:
    """Stellt die Verbindung zum MQTT-Broker her."""

    def __init__(self, broker, port):

        self.broker = broker
        self.port = port

        self.client = mqtt.Client()

        print("✅ MQTTClient erstellt")

    def connect(self):
        """Stellt die Verbindung zum MQTT-Broker her."""

        try:
            self.client.connect(
                self.broker,
                self.port,
                keepalive=60
            )

            print("✅ Mit MQTT-Broker verbunden")

        except Exception as error:
            print(f"❌ MQTT-Verbindung fehlgeschlagen: {error}")
            raise

    def publish(self, topic, message):
        """Sendet eine Nachricht an den MQTT-Broker."""

        self.client.publish(topic, message)

        print(f"📤 Gesendet: {topic} -> {message}")

    def disconnect(self):
        """Trennt die Verbindung zum MQTT-Broker."""

        self.client.disconnect()

        print("🔌 MQTT-Verbindung getrennt")