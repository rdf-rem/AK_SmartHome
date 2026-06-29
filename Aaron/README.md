# 🏠 Aaron's Smart-Home Dashboard

Interaktives Web-Dashboard zur Visualisierung und Kontrolle des Smart-Home-Systems in Echtzeit.

## Technologie

- **Backend:** Flask + Flask-SocketIO
- **Frontend:** HTML5 + CSS3 + JavaScript
- **Real-time:** WebSocket (Socket.IO)
- **MQTT-Integration:** paho-mqtt
- **Design:** Responsive & Modern

## Features

### 📊 Visualisierung
- **Wohnzimmer:** Licht, Rollos (Slider), Temperatur, Luftfeuchtigkeit
- **Schlafzimmer:** Licht, Bewegungsmelder (PIR), Temperatur
- **Küche:** Licht, Temperatur
- **Live MQTT-Status:** Anzeige des Broker-Verbindungsstatus
- **Gesterkennung:** Anzeige der erkannten Gesten in Echtzeit

### 🎮 Steuerung
- Licht ein/aus schalten
- Rollos öffnen/schließen (mit Slider)
- Responsive Design für Desktop & Mobile

### 📡 Real-time Updates
- WebSocket-Verbindung zum Backend
- Automatische UI-Updates bei Datenaenderung
- 2-Sekunden-Refresh-Zyklus

## Installation

### Voraussetzungen
- Python 3.8+
- Installierte Pakete: `flask`, `flask-socketio`, `python-socketio`, `python-engineio`, `paho-mqtt`

Installation bereits durchgeführt (siehe Setup-Anleitung).

## Starten

### Terminal-Befehl

```bash
cd c:\Users\diosd\Documents\VisualStudioCode\AK_SmartHome\Aaron

# Mit dem Python-Executable der virtuellen Umgebung:
c:/Users/diosd/Documents/VisualStudioCode/AK_SmartHome/Aaron/.venv/Scripts/python.exe dashboard/app.py
```

### Browser öffnen

Nach dem Start öffne deinen Browser und gehe zu:
```
http://127.0.0.1:5000
```

### Terminal-Output

```
=== Smart-Home Dashboard ===
🌐 Starte auf http://127.0.0.1:5000
📡 MQTT Broker: broker.hivemq.com:1883

✓ Running on http://127.0.0.1:5000
✓ MQTT verbunden
```

## MQTT Integration

### Empfangene Topics

Das Dashboard abonniert alle Topics unter `aaron/smarthome/#`:

```
aaron/smarthome/gesture          → Gesterkennung
aaron/smarthome/livingroom/light → Wohnzimmerlicht
aaron/smarthome/bedroom/light    → Schlafzimmerlicht
aaron/smarthome/kitchen/light    → Küchenlicht
aaron/smarthome/livingroom/blinds → Rollos
aaron/smarthome/kitchen/temperature → Temperatur (Küche)
aaron/smarthome/bedroom/temperature → Temperatur (Schlafzimmer)
aaron/smarthome/bedroom/pir      → Bewegungsmelder
aaron/smarthome/livingroom/humidity → Luftfeuchtigkeit
```

### Payload-Format

Beispiel für Gesten:
```json
{
  "gesture": "PEACE",
  "timestamp": 1698765432.123
}
```

Beispiel für Licht:
```json
{
  "state": true,
  "timestamp": 1698765432.123
}
```

Beispiel für Temperatur:
```json
{
  "value": 22.5,
  "timestamp": 1698765432.123
}
```

## Dateien & Struktur

```
dashboard/
├── app.py                          # Flask Backend + MQTT Client
├── templates/
│   └── index.html                  # Dashboard HTML UI
└── static/
    ├── style.css                   # Styling & Layout
    └── dashboard.js                # WebSocket & Interaktion
```

## Features im Detail

### Licht-Steuerung
- Button zeigt aktuellen Zustand (EIN/AUS)
- Click sendet Toggle-Befehl an Backend

### Rollo-Slider
- 0-100% Schieberegler
- Live-Anzeige des Prozentsatzes
- Status-Text: Geschlossen / Teilweise offen / Geöffnet

### Sensoren
- Temperatur mit Dezimalanzeige
- Luftfeuchtigkeit als Prozentangabe
- PIR-Sensor mit Animations-Indicator

### Gesterkennung
- Zeigt letzte erkannte Geste für 3 Sekunden
- Automatisches Zurücksetzen

## Fehlerbehebung

| Problem | Lösung |
|---------|--------|
| Port 5000 bereits in Benutzung | Andere App schließen oder anderen Port verwenden: `socketio.run(app, port=5001)` |
| MQTT-Verbindung fehlgeschlagen | Broker erreichbar? `ping broker.hivemq.com` |
| Dashboard lädt nicht | Browser Cache leeren (Ctrl+Shift+Delete) |
| WebSocket-Fehler | Browser-Konsole überprüfen (F12 → Console) |
| Daten aktualisieren nicht | ESP32/MediaPipe publizieren korrekt? MQTT-Tester verwenden |

## Backend-Anpassungen

### Neuen Room hinzufügen

In `app.py`:
```python
dashboard_state = {
    ...
    "neuer_raum": {
        "light": False,
        "temperature": 0
    }
}
```

### Neues Topic verarbeiten

In `on_mqtt_message()`:
```python
elif "neuer_topic" in topic:
    value = payload.get("value")
    dashboard_state["raum"]["device"] = value
    socketio.emit('update', dashboard_state, broadcast=True)
```

### Broker wechseln

In `app.py`:
```python
MQTT_BROKER = "dein-broker.com"  # Ändern
MQTT_PORT = 1883
```

## Frontend-Anpassungen

### CSS-Farben ändern

In `style.css`:
```css
:root {
    --primary: #2196F3;    /* Hauptfarbe */
    --success: #4CAF50;    /* Erfolg */
    --danger: #f44336;     /* Fehler */
    ...
}
```

### Neues Device hinzufügen

In `index.html`:
```html
<div class="device neues-device">
    <div class="device-icon">🔌</div>
    <div class="device-info">
        <h3>Gerät</h3>
        <p id="status">Status</p>
    </div>
</div>
```

## Performance-Tipps

- Refresh-Zyklus anpassen (dashboard.js Zeile ~200)
- Min-Detection-Confidence in MediaPipe erhöhen
- MQTT QoS-Level überprüfen

## Integration mit MediaPipe

MediaPipe publiziert Gesten zu `aaron/smarthome/gesture`:
- Diese werden im Dashboard in Echtzeit angezeigt
- Optional können darauf automatische Aktionen reagieren

## Integration mit ESP32

ESP32 sollte folgende Topics abonnieren:
- `aaron/smarthome/*/light` → LED steuern
- `aaron/smarthome/livingroom/blinds` → Servo bewegen
- `aaron/smarthome/gesture` → Spezialaktionen

## Weitere Ressourcen

- [Flask-SocketIO Dokumentation](https://flask-socketio.readthedocs.io/)
- [Socket.IO Client](https://socket.io/)
- [MQTT Topics Best Practice](https://mosquitto.org/documentation/)

---

**Aaron's Smart-Home System** | Projektabgabe 2026
