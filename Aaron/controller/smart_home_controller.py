"""
smart_home_controller.py

Verarbeitet empfangene Gesten und führt Aktionen aus.

Autor: Aaron
Unterstützung: ChatGPT
Projekt: Smart Home Steuerung mittels Gestenerkennung
"""

from devices.light import Light
from devices.blinds import Blinds
from devices.temperature import Temperature
from devices.motion_sensor import MotionSensor


class SmartHomeController:

    def __init__(self):

        self.light = Light()
        self.blinds = Blinds()
        self.temperature = Temperature()
        self.motion_sensor = MotionSensor()

        self.actions = {
            "Open_Palm": self.light_on,
            "Closed_Fist": self.light_off,
            "Thumb_Up": self.blinds_open,
            "Victory": self.blinds_close
        }

    def handle_gesture(self, gesture):
        """Führt die zur Geste gehörende Aktion aus."""

        action = self.actions.get(gesture)

        if action:
            action()
        else:
            print("❓ Unbekannte Geste")

    def light_on(self):
        self.light.on()

    def light_off(self):
        self.light.off()

    def blinds_open(self):
        self.blinds.open()

    def blinds_close(self):
        self.blinds.close()