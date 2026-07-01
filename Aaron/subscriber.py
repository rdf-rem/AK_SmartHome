"""
subscriber.py

Empfängt Gesten vom MQTT-Broker.

Autor: Aaron
Unterstützung: ChatGPT
Projekt: Smart Home Steuerung mittels Gestenerkennung
"""

import paho.mqtt.client as mqtt

from config import Config
from controller.smart_home_controller import SmartHomeController


config = Config()
controller = SmartHomeController()


def on_connect(client, userdata, flags, reason_code, properties=None):
    """Wird nach erfolgreicher Verbindung aufgerufen."""

    print("✅ Mit MQTT-Broker verbunden")

    client.subscribe(config.gesture_topic)
    client.subscribe(config.temperature_topic)
    client.subscribe(config.motion_topic)

    print("👂 Lausche auf:")

    print(f"   🎯 Gesten:      {config.gesture_topic}")
    print(f"   🌡️ Temperatur: {config.temperature_topic}")
    print(f"   🚶 Bewegung:   {config.motion_topic}")


def on_message(client, userdata, message):
    """Wird bei jeder empfangenen Nachricht aufgerufen."""

    topic = message.topic
    payload = message.payload.decode()

    print(f"\n📩 [{topic}] {payload}")

    if topic == config.gesture_topic:

        controller.handle_gesture(payload)

    elif topic == config.temperature_topic:

        controller.temperature.update(float(payload))

    elif topic == config.motion_topic:

        controller.motion_sensor.update(payload == "motion")


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