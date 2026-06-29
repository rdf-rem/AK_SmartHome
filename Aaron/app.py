"""
Smart-Home Dashboard Backend
Flask-App mit MQTT-Integration und WebSocket für Real-time Updates
"""

from flask import Flask, render_template
from flask_socketio import SocketIO, emit, join_room, leave_room
import paho.mqtt.client as mqtt
import json
import threading
from datetime import datetime

app = Flask(__name__, 
            template_folder='templates',
            static_folder='static')
app.config['SECRET_KEY'] = 'aaron-smarthome-secret'
socketio = SocketIO(app, cors_allowed_origins="*")

# MQTT Konfiguration
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883

# Dashboard State (speichert aktuelle Zustände)
dashboard_state = {
    "livingroom": {
        "light": False,
        "blinds": 0,  # 0-100%
        "temperature": 0,
        "humidity": 0
    },
    "bedroom": {
        "light": False,
        "pir": False,
        "temperature": 0
    },
    "kitchen": {
        "light": False,
        "temperature": 0
    },
    "last_gesture": None,
    "mqtt_status": "DISCONNECTED"
}

# MQTT Client
mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)

def on_mqtt_connect(client, userdata, flags, rc):
    """MQTT Verbindung hergestellt"""
    if rc == 0:
        dashboard_state["mqtt_status"] = "CONNECTED"
        print("✓ MQTT verbunden")
        # Abonniere alle Aaron Topics
        client.subscribe("aaron/smarthome/#", qos=1)
        socketio.emit('status', {'mqtt': 'CONNECTED'}, broadcast=True)
    else:
        dashboard_state["mqtt_status"] = "FAILED"
        socketio.emit('status', {'mqtt': f'FAILED ({rc})'}, broadcast=True)

def on_mqtt_message(client, userdata, msg):
    """MQTT Nachricht empfangen"""
    try:
        topic = msg.topic
        payload = json.loads(msg.payload.decode())
        
        # Gesten verarbeiten
        if "gesture" in topic:
            gesture = payload.get("gesture", "UNKNOWN")
            dashboard_state["last_gesture"] = gesture
            socketio.emit('gesture', {'gesture': gesture}, broadcast=True)
            print(f"📨 Geste: {gesture}")
        
        # Lichtzustände
        elif "light" in topic:
            state = payload.get("state", False)
            if "livingroom" in topic:
                dashboard_state["livingroom"]["light"] = state
            elif "bedroom" in topic:
                dashboard_state["bedroom"]["light"] = state
            elif "kitchen" in topic:
                dashboard_state["kitchen"]["light"] = state
            socketio.emit('update', dashboard_state, broadcast=True)
        
        # Rollos
        elif "blinds" in topic:
            value = payload.get("value", 0)
            dashboard_state["livingroom"]["blinds"] = value
            socketio.emit('update', dashboard_state, broadcast=True)
        
        # Temperatur
        elif "temperature" in topic:
            temp = payload.get("value", 0)
            if "kitchen" in topic:
                dashboard_state["kitchen"]["temperature"] = temp
            elif "bedroom" in topic:
                dashboard_state["bedroom"]["temperature"] = temp
            else:
                dashboard_state["livingroom"]["temperature"] = temp
            socketio.emit('update', dashboard_state, broadcast=True)
        
        # Bewegungsmelder (PIR)
        elif "pir" in topic:
            detected = payload.get("detected", False)
            dashboard_state["bedroom"]["pir"] = detected
            socketio.emit('update', dashboard_state, broadcast=True)
        
        # Luftfeuchtigkeit
        elif "humidity" in topic:
            humidity = payload.get("value", 0)
            dashboard_state["livingroom"]["humidity"] = humidity
            socketio.emit('update', dashboard_state, broadcast=True)
    
    except Exception as e:
        print(f"Fehler beim Verarbeiten: {e}")

def on_mqtt_disconnect(client, userdata, rc):
    """MQTT Verbindung getrennt"""
    if rc != 0:
        dashboard_state["mqtt_status"] = "DISCONNECTED"
        socketio.emit('status', {'mqtt': 'DISCONNECTED'}, broadcast=True)

# MQTT Setup
mqtt_client.on_connect = on_mqtt_connect
mqtt_client.on_message = on_mqtt_message
mqtt_client.on_disconnect = on_mqtt_disconnect

def connect_mqtt():
    """MQTT im Background Thread verbinden"""
    try:
        mqtt_client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
        mqtt_client.loop_forever()
    except Exception as e:
        print(f"MQTT Fehler: {e}")

@app.route('/')
def index():
    """Dashboard Homepage"""
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    """WebSocket Verbindung hergestellt"""
    print(f"✓ Client verbunden")
    emit('status', {'mqtt': dashboard_state['mqtt_status']})
    emit('update', dashboard_state)

@socketio.on('disconnect')
def handle_disconnect():
    """WebSocket Verbindung getrennt"""
    print(f"✗ Client getrennt")

@socketio.on('request_state')
def handle_request_state():
    """Client fordert aktuellen State an"""
    emit('update', dashboard_state)

@socketio.on('control')
def handle_control(data):
    """Empfange Kontrolbefehle vom Dashboard"""
    action = data.get('action')
    room = data.get('room')
    value = data.get('value')
    
    print(f"🎮 Kontrolbefehl: {action} in {room} = {value}")
    
    # Hier könnten Befehle an MQTT gesendet werden
    # Beispiel: mqtt_client.publish(f"aaron/smarthome/{room}/control", json.dumps({...}))

if __name__ == '__main__':
    # MQTT im Background starten
    mqtt_thread = threading.Thread(target=connect_mqtt, daemon=True)
    mqtt_thread.start()
    
    print("=== Smart-Home Dashboard ===")
    print(f"🌐 Starte auf http://127.0.0.1:5000")
    print(f"📡 MQTT Broker: {MQTT_BROKER}:{MQTT_PORT}\n")
    
    # Flask-SocketIO Server starten
    socketio.run(app, host='127.0.0.1', port=5000, debug=True, use_reloader=False)
