"""
gesture_recognition.py

Hauptprogramm.

Startet Kamera und Gestenerkennung.

Autor: Aaron
Unterstützung: ChatGPT
Projekt: Smart Home Steuerung mittels Gestenerkennung
"""

import cv2
import time

from gesture.camera import Camera
from gesture.recognizer import Recognizer

from config import Config
from mqtt.mqtt_client import MQTTClient


def main():

    config = Config()

    camera = Camera(
        config.camera_index,
        config.camera_flip
    )

    recognizer = Recognizer(config.model_path)

    mqtt = MQTTClient(
        config.mqtt_broker,
        config.mqtt_port
    )

    last_gesture = ""
    last_gesture_time = 0

    try:

        mqtt.connect()

        print("✅ System gestartet")
        print("Drücke q zum Beenden")

        while True:

            frame = camera.read()

            if frame is None:
                break

            gesture = recognizer.recognize(frame)

            if gesture:

                current_time = time.time()

                if (
                    gesture != last_gesture
                    or current_time - last_gesture_time >= config.cooldown
                ):

                    print("👉", gesture)

                    mqtt.publish(
                        config.gesture_topic,
                        gesture
                    )

                    last_gesture = gesture
                    last_gesture_time = current_time

                cv2.putText(
                    frame,
                    gesture,
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2
                )

            cv2.imshow("Gesture Recognition", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    except Exception as error:
        print(f"❌ Fehler: {error}")

    finally:

        mqtt.disconnect()

        camera.release()
        cv2.destroyAllWindows()

        print("Programm beendet")


if __name__ == "__main__":
    main()