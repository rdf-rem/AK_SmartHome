"""
light.py

Steuert das Licht.

Autor: Aaron
Unterstützung: ChatGPT
Projekt: Smart Home Steuerung mittels Gestenerkennung
"""


class Light:

    def __init__(self):
        self.is_on = False

    def on(self):

        if self.is_on:
            print("💡 Licht ist bereits EIN")
            return

        self.is_on = True
        print("💡 Licht EIN")

    def off(self):

        if not self.is_on:
            print("💡 Licht ist bereits AUS")
            return

        self.is_on = False
        print("💡 Licht AUS")