"""
temperature.py

Verwaltet den Temperaturwert.

Autor: Aaron
Unterstützung: ChatGPT
Projekt: Smart Home Steuerung mittels Gestenerkennung
"""


class Temperature:

    def __init__(self):
        self.value = 0.0

    def update(self, value):
        self.value = value
        print(f"🌡️ Temperatur: {self.value:.1f} °C")