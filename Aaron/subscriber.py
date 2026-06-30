"""
subscriber.py

Empfängt Gesten vom MQTT-Broker.

Autor: Aaron
Unterstützung: ChatGPT
Projekt: Smart Home Steuerung mittels Gestenerkennung
"""

import paho.mqtt.client as mqtt

from config import Config


config = Config()


def on_connect(client, userdata, flags, reason_code, properties=None):
    """Wird nach erfolgreicher Verbindung aufgerufen."""

    print("✅ Mit MQTT-Broker verbunden")

    client.subscribe(config.gesture_topic)

    print(f"👂 Lausche auf: {config.gesture_topic}")


def on_message(client, userdata, message):
    """Wird bei jeder empfangenen Nachricht aufgerufen."""

    gesture = message.payload.decode("utf-8")

    print(f"📩 Empfangen: {gesture}")


def main():

    client = mqtt.Client()

    client.on_connect = on_connect
    client.on_message = on_message

    print("Verbinde...")

    client.connect(
        config.mqtt_broker,
        config.mqtt_port,
        keepalive=60
    )

    client.loop_forever()


if __name__ == "__main__":
    main()