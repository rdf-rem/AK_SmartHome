"""
motion_sensor.py

Verwaltet den Bewegungsmelder.

Autor: Aaron
Unterstützung: ChatGPT
Projekt: Smart Home Steuerung mittels Gestenerkennung
"""


class MotionSensor:

    def __init__(self):
        self.motion_detected = False

    def update(self, detected):

        self.motion_detected = detected

        if detected:
            print("🚶 Bewegung erkannt")
        else:
            print("😴 Keine Bewegung")