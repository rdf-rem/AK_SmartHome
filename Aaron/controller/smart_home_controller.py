"""
smart_home_controller.py

Verarbeitet empfangene Gesten und führt Aktionen aus.

Autor: Aaron
Unterstützung: ChatGPT
Projekt: Smart Home Steuerung mittels Gestenerkennung
"""

from devices.light import Light
from devices.music import Music
from devices.tv import TV


class SmartHomeController:

    def __init__(self):

        self.actions = {
            "Open_Palm": self.light_on,
            "Closed_Fist": self.light_off,
            "Thumb_Up": self.music_on,
            "Victory": self.tv_mode
        }

    def handle_gesture(self, gesture):
        """Führt die zur Geste gehörende Aktion aus."""

        action = self.actions.get(gesture)

        if action:
            action()
        else:
            print("❓ Unbekannte Geste")

    def light_on(self):
        print("💡 Licht EIN")

    def light_off(self):
        print("💡 Licht AUS")

    def music_on(self):
        print("🎵 Musik EIN")

    def tv_mode(self):
        print("📺 TV-Modus")