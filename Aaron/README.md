## Smart Home Steuerung mittels Gestenerkennung

# Quickstart

1. MQTT starten                         -> subscriber.py
2. Sensorsimulation aktivieren          -> sensor_publisher.py
3. Dashboard aktivieren                 -> dashboard.py
4. Gestenerkennung/Kamera starten       -> app.py
5. Dashboard im Browser öffnen (auf dem Handy ist die IP Adresse des Rechners notwendig)

---

# Projektbeschreibung

Dieses Projekt demonstriert die Steuerung eines Smart Homes mithilfe von Handgesten. Die Gestenerkennung erfolgt über eine Webcam und MediaPipe. Erkannte Gesten werden über das MQTT-Protokoll übertragen und steuern verschiedene Smart-Home-Komponenten wie Licht und Rollos. Zusätzlich werden Temperatur- und Bewegungsdaten simuliert und in einem webbasierten Dashboard visualisiert.

Das Projekt entstand im Rahmen des Moduls **Angewandte Kommunikation**.

---

# Projektfunktionen

Folgende Funktionen wurden umgesetzt:

- Handgestenerkennung mittels MediaPipe
- Steuerung von Licht und Rollos über Gesten
- MQTT-Kommunikation zwischen den Komponenten
- Simulation eines Temperatursensors
- Simulation eines Bewegungsmelders
- Smart-Home-Controller zur Verarbeitung aller Befehle
- Web-Dashboard mit Live-Anzeige
- Responsive Benutzeroberfläche im Dark Theme

---

# Verwendete Technologien

- Python 3.14
- MediaPipe
- OpenCV
- Flask
- MQTT (Paho MQTT)
- HTML5
- CSS3
- JavaScript
- JSON

---

# Projektstruktur

```
AK_SmartHome/
│
├── app.py
├── dashboard.py
├── subscriber.py
├── sensor_publisher.py
├── config.py
├── config.json
├── README.md
│
├── controller/
│       smart_home_controller.py
│
├── devices/
│       light.py
│       blinds.py
│       temperature.py
│       motion_sensor.py
│
├── gesture/
│       camera.py
│       recognizer.py
│       gesture_recognition.py
│
├── mqtt/
│       mqtt_client.py
│
├── templates/
│       index.html
│
├── static/
│       style.css
│       dashboard.js
│
├── data/
│       state.json
│
└── models/
        gesture_recognizer.task
```

---

# Installation

Repository herunterladen oder klonen.

Benötigte Bibliotheken installieren:

```bash
pip install mediapipe
pip install opencv-python
pip install flask
pip install paho-mqtt
```

---

# Projekt starten

## MQTT-Broker starten

Es wird ein MQTT-Broker benötigt (z. B. Mosquitto).

---

## Subscriber starten

```bash
python subscriber.py
```

---

## Sensor-Simulation starten

```bash
python sensor_publisher.py
```

---

## Dashboard starten

```bash
python dashboard.py
```

Dashboard im Browser öffnen:

```
http://127.0.0.1:5000
```

---

## Gestenerkennung starten

```bash
python app.py
```

---

# Gestensteuerung

| Geste | Funktion |
|--------|----------|
| Open_Palm | Licht einschalten |
| Closed_Fist | Licht ausschalten |
| Thumb_Up | Rollo öffnen |
| Victory | Rollo schließen |

---

# MQTT-Kommunikation

Verwendete Topics:

| Topic | Beschreibung |
|--------|--------------|
| aaron/smarthome/gesture | Gestenerkennung |
| aaron/smarthome/temperature | Temperatur |
| aaron/smarthome/motion | Bewegungsmelder |

---

# Dashboard

Das Dashboard zeigt den aktuellen Zustand des Smart Homes in Echtzeit.

Angezeigt werden:

- Lichtstatus
- Rollostatus
- Temperatur
- Bewegung
- Letzte erkannte Geste
- Systemstatus
- Uhrzeit

Die Anzeige wird automatisch in regelmäßigen Abständen aktualisiert, sodass Änderungen nahezu in Echtzeit sichtbar werden.

---

# Projektablauf

```
Kamera

↓

MediaPipe

↓

Gestenerkennung

↓

MQTT

↓

SmartHomeController

↓

Geräte

↓

Dashboard
```

---

# Autoren

**Aaron**

Projekt im Rahmen des Moduls **Angewandte Kommunikation**

Das Projekt wurde unter Verwendung von ChatGPT als unterstützendes Werkzeug bei Konzeption, Implementierung und Dokumentation entwickelt.

---

# Bekannte Einschränkungen

- Die Sensoren werden derzeit simuliert.
- Das Dashboard dient der Visualisierung und Steuerung innerhalb des Projekts.
- Für die Gestenerkennung wird eine funktionierende Webcam benötigt.

---

# Lizenz

Dieses Projekt dient ausschließlich Ausbildungs- und Demonstrationszwecken.