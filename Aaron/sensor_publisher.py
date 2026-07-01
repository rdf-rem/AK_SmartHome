"""
sensor_publisher.py

Simuliert Temperatur- und Bewegungsdaten
für das Smart-Home-System.

Autor: Aaron
Unterstützung: ChatGPT
Projekt: Smart Home Steuerung mittels Gestenerkennung
"""

import random
import time

import paho.mqtt.client as mqtt

from config import Config


config = Config()


def main():

    client = mqtt.Client()

    print("Verbinde...")

    client.connect(
        config.mqtt_broker,
        config.mqtt_port,
        keepalive=60
    )

    print("✅ Sensor-Simulation gestartet")

    motion = False

    while True:

        # Temperatur simulieren
        temperature = round(random.uniform(20.0, 25.0), 1)

        client.publish(
            config.temperature_topic,
            str(temperature)
        )

        print(f"🌡️ Temperatur gesendet: {temperature} °C")

        # Bewegung simulieren (wechselt zwischen Bewegung und keiner Bewegung)
        motion = not motion

        if motion:
            payload = "motion"
        else:
            payload = "clear"

        client.publish(
            config.motion_topic,
            payload
        )

        print(f"🚶 Bewegung gesendet: {payload}")

        print("------------------------------")

        time.sleep(15)  # Temperatur und Bewegungsstatus werden alle 15 Sekunden aktualisiert.


if __name__ == "__main__":
    main()