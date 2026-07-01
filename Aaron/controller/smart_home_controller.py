"""
smart_home_controller.py

Verarbeitet empfangene Gesten und führt Aktionen aus.

Autor: Aaron
Unterstützung: ChatGPT
Projekt: Smart Home Steuerung mittels Gestenerkennung
"""

import json
from pathlib import Path

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

        self.last_gesture = "-"

        self.state_file = Path("data/state.json")

        self.actions = {
            "Open_Palm": self.light_on,
            "Closed_Fist": self.light_off,
            "Thumb_Up": self.blinds_open,
            "Victory": self.blinds_close
        }

    def handle_gesture(self, gesture):
        """Führt die zur Geste gehörende Aktion aus."""

        self.last_gesture = gesture

        action = self.actions.get(gesture)

        if action:
            action()
            self.save_state()
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

    def get_state(self):
        """Gibt den aktuellen Zustand des Smart Homes zurück."""

        return {
            "light": self.light.is_on,
            "blinds": self.blinds.is_open,
            "temperature": self.temperature.value,
            "motion": self.motion_sensor.detected,
            "last_gesture": self.last_gesture
        }

    def save_state(self):
        """Speichert den aktuellen Zustand des Smart Homes."""

        self.state_file.parent.mkdir(exist_ok=True)

        with open(self.state_file, "w", encoding="utf-8") as file:
            json.dump(
                self.get_state(),
                file,
                indent=4
            )