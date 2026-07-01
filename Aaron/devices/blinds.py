"""
blinds.py

Steuert das Rollo.

Autor: Aaron
Unterstützung: ChatGPT
Projekt: Smart Home Steuerung mittels Gestenerkennung
"""


class Blinds:

    def __init__(self):
        self.is_open = False

    def open(self):

        if self.is_open:
            print("🪟 Rollo ist bereits geöffnet")
            return

        self.is_open = True
        print("🪟 Rollo geöffnet")

    def close(self):

        if not self.is_open:
            print("🪟 Rollo ist bereits geschlossen")
            return

        self.is_open = False
        print("🪟 Rollo geschlossen")