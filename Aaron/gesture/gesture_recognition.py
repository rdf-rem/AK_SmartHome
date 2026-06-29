"""
gesture_recognition.py

Hauptprogramm.

Startet Kamera und Gestenerkennung.

Autor: Aaron
Projekt: Smart Home Steuerung mittels Gestenerkennung
"""

import cv2

from camera import Camera
from recognizer import Recognizer


camera = Camera()
recognizer = Recognizer("models/gesture_recognizer.task")

print("✅ System gestartet")
print("Drücke q zum Beenden")

last_gesture = ""

while True:

    frame = camera.read()

    if frame is None:
        break

    gesture = recognizer.recognize(frame)

    if gesture:

        if gesture != last_gesture:

            print("👉", gesture)

            last_gesture = gesture

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

camera.release()

print("Programm beendet")