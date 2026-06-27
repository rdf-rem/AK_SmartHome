Wokwi Smart-Home Beispiel

Dieses Projekt enthält eine einfache Simulation für ein Smart-Home-Szenario mit:
- Arduino Uno
- Taster für Türstatus
- Potentiometer für Helligkeit
- zwei LEDs als Zustandsanzeige

Dateien:
- diagram.json: Wokwi-Schaltplan
- sketch.ino: Arduino-Code

So verwendest du es:
1. Öffne die Datei diagram.json in Wokwi.
2. Lade sketch.ino als Arduino-Sketch.
3. Starte die Simulation.


Schaltplan und Anschlüsse:
- Arduino Pin 2 -> Taster (einseitig)
- Taster anderer Seite -> GND
- Arduino Pin 9 -> 220-Ohm-Widerstand -> rote LED (Anode)
- rote LED Kathode -> GND
- Arduino Pin 10 -> 220-Ohm-Widerstand -> grüne LED (Anode)
- grüne LED Kathode -> GND
- Arduino A0 -> Potentiometer Signal
- Potentiometer VCC -> 5V
- Potentiometer GND -> GND


Hier ist die kurze Checkliste für Wokwi:

1. Öffne diagram.json in Wokwi.
2. Lade sketch.ino als Arduino-Sketch.
3. Stelle sicher, dass der Arduino Uno ausgewählt ist.
4. Klicke auf Start/Run.
5. Teste:
- Taster drücken → Zustand wechselt zwischen offen und geschlossen
- Potentiometer drehen → Helligkeit der LED ändert sich
6. Im Serial Monitor solltest du Nachrichten wie:
- „Status: Tür offen“
- „Status: Tür geschlossen“


Wenn etwas nicht funktioniert, schau zuerst auf:
- richtige Pin-Verbindungen im Diagramm
- ob die LED korrekt angeschlossen ist
- ob der Sketch wirklich zu Arduino Uno passt


Problem: Tür geht auf und zu (LEDs blinken entsprechend)
Fehlersuche abgebrochen, da nicht wirklich eigener Teil des Projekt
-> weiter mit anderen Projektpunkten