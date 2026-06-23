import json
import threading
from flask import Flask, jsonify, render_template_string
import paho.mqtt.client as mqtt

app = Flask(__name__)
state = {
    "light": "OFF",
    "blinds": "CLOSED",
    "temperature": None,
    "pir": "0",
    "gesture": None,
}

MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
TOPICS = [
    ("home/livingroom/light", 0),
    ("home/livingroom/blinds", 0),
    ("home/kitchen/temperature", 0),
    ("home/bedroom/pir", 0),
    ("home/gesture", 0),
]

client = mqtt.Client()


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Dashboard MQTT connected")
        for topic, qos in TOPICS:
            client.subscribe(topic, qos)
    else:
        print("Dashboard MQTT connection failed", rc)


def on_message(client, userdata, msg):
    payload = msg.payload.decode("utf-8")
    if msg.topic == "home/livingroom/light":
        state["light"] = payload
    elif msg.topic == "home/livingroom/blinds":
        state["blinds"] = payload
    elif msg.topic == "home/kitchen/temperature":
        state["temperature"] = payload
    elif msg.topic == "home/bedroom/pir":
        state["pir"] = payload
    elif msg.topic == "home/gesture":
        state["gesture"] = payload


@app.route("/api/state")
def api_state():
    return jsonify(state)


@app.route("/")
def index():
    return render_template_string(
        """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>Smart Home Dashboard</title>
  <style>
    body { font-family: Arial, sans-serif; background: #f4f4f9; color: #222; padding: 20px; }
    .panel { border-radius: 12px; background: white; padding: 20px; margin-bottom: 15px; box-shadow: 0 2px 8px rgba(0,0,0,0.12); }
    .panel h2 { margin-top: 0; }
    .status { font-size: 1.25em; }
  </style>
</head>
<body>
  <h1>Smart Home Dashboard</h1>
  <div class="panel">
    <h2>Living Room</h2>
    <p class="status">Light: <strong id="light">OFF</strong></p>
    <p class="status">Blinds: <strong id="blinds">CLOSED</strong></p>
  </div>
  <div class="panel">
    <h2>Sensor Data</h2>
    <p class="status">Temperature: <strong id="temperature">--</strong> °C</p>
    <p class="status">Motion: <strong id="pir">No</strong></p>
    <p class="status">Last gesture: <strong id="gesture">--</strong></p>
  </div>
  <script>
    async function refresh() {
      const res = await fetch('/api/state');
      const data = await res.json();
      document.getElementById('light').innerText = data.light;
      document.getElementById('blinds').innerText = data.blinds;
      document.getElementById('temperature').innerText = data.temperature || '--';
      document.getElementById('pir').innerText = data.pir === '1' ? 'Yes' : 'No';
      document.getElementById('gesture').innerText = data.gesture || '--';
    }
    setInterval(refresh, 2000);
    refresh();
  </script>
</body>
</html>
        """
    )


def mqtt_thread():
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_forever()


if __name__ == "__main__":
    thread = threading.Thread(target=mqtt_thread, daemon=True)
    thread.start()
    app.run(host="0.0.0.0", port=5000)
