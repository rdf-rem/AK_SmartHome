#====================================
# Smart Home Projekt
# MediaPipe Gestensteuerung -> MQTT
#====================================
# Benoetigte Pakete installieren:
#   pip install mediapipe opencv-python paho-mqtt
#
# Beim ersten Start wird automatisch das MediaPipe-Modell
# "gesture_recognizer.task" heruntergeladen (ca. 8 MB).

import os
import time
import urllib.request

import cv2
import mediapipe as mp
from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision
import paho.mqtt.client as mqtt

#------------------------------------
# MQTT-Konfiguration (gleiche Werte wie im ESP32-Sketch)
#------------------------------------
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_CLIENT_ID = "mediapipe-ak_smarthome"

PREFIX = "ak_smarthome"
TOPIC_LIGHT = f"{PREFIX}/home/livingroom/light"
TOPIC_BLINDS = f"{PREFIX}/home/livingroom/blinds"

#------------------------------------
# Geste -> Aktion zuordnen
# (MediaPipe-Gestennamen -> (Topic, Payload))
#------------------------------------
GESTURE_ACTIONS = {
    "Thumb_Up":    (TOPIC_BLINDS, "OPEN"),   # Daumen hoch    -> Rollo hoch
    "Thumb_Down":  (TOPIC_BLINDS, "CLOSE"),  # Daumen runter  -> Rollo runter
    "Closed_Fist": (TOPIC_LIGHT,  "OFF"),    # Faust          -> Licht aus
    "Victory":     (TOPIC_LIGHT,  "ON"),     # Zeige-/Mittelfinger -> Licht an
}

# Mindest-Konfidenz, damit eine Geste als erkannt gilt
CONFIDENCE_THRESHOLD = 0.6

# Wartezeit zwischen zwei MQTT-Nachrichten derselben Geste (Sekunden),
# damit nicht bei jedem Kamera-Frame erneut gesendet wird
COOLDOWN_SECONDS = 1.5

#------------------------------------
# Modell automatisch herunterladen, falls nicht vorhanden
#------------------------------------
MODEL_PATH = "gesture_recognizer.task"
MODEL_URL = (
    "https://storage.googleapis.com/mediapipe-models/"
    "gesture_recognizer/gesture_recognizer/float16/1/"
    "gesture_recognizer.task"
)

def sicherstellen_modell_vorhanden():
    if not os.path.exists(MODEL_PATH):
        print("Lade MediaPipe-Gestenmodell herunter ...")
        urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)
        print("Modell heruntergeladen.")

#------------------------------------
# MQTT verbinden
#------------------------------------
def mqtt_verbinden():
    client = mqtt.Client(client_id=MQTT_CLIENT_ID)

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("MQTT verbunden mit", MQTT_BROKER)
        else:
            print("MQTT-Verbindung fehlgeschlagen, rc =", rc)

    client.on_connect = on_connect
    client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
    client.loop_start()  # laeuft im Hintergrund, verarbeitet Verbindung
    return client

#------------------------------------
# Hauptprogramm
#------------------------------------
def main():
    sicherstellen_modell_vorhanden()
    mqtt_client = mqtt_verbinden()

    # GestureRecognizer im VIDEO-Modus erstellen
    base_options = mp_python.BaseOptions(model_asset_path=MODEL_PATH)
    options = vision.GestureRecognizerOptions(
        base_options=base_options,
        running_mode=vision.RunningMode.VIDEO,
        num_hands=1,
    )
    recognizer = vision.GestureRecognizer.create_from_options(options)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Konnte Webcam nicht oeffnen.")
        return

    print("Gestensteuerung laeuft. 'q' druecken zum Beenden.")

    last_sent_gesture = None
    last_sent_time = 0.0

    while True:
        ok, frame = cap.read()
        if not ok:
            print("Kein Kamerabild erhalten.")
            break

        # Spiegeln, damit die Anzeige sich wie ein Spiegel verhaelt
        frame = cv2.flip(frame, 1)

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

        timestamp_ms = int(time.time() * 1000)
        result = recognizer.recognize_for_video(mp_image, timestamp_ms)

        erkannte_geste = None
        konfidenz = 0.0

        if result.gestures:
            top_gesture = result.gestures[0][0]
            erkannte_geste = top_gesture.category_name
            konfidenz = top_gesture.score

        # Anzeige auf dem Kamerabild (zur Kontrolle waehrend der Entwicklung)
        anzeige_text = f"{erkannte_geste} ({konfidenz:.2f})" if erkannte_geste else "keine Geste"
        cv2.putText(frame, anzeige_text, (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Nur reagieren, wenn Geste bekannt ist und Konfidenz hoch genug
        if erkannte_geste in GESTURE_ACTIONS and konfidenz >= CONFIDENCE_THRESHOLD:
            jetzt = time.time()
            neue_geste = erkannte_geste != last_sent_gesture
            cooldown_abgelaufen = (jetzt - last_sent_time) >= COOLDOWN_SECONDS

            if neue_geste or cooldown_abgelaufen:
                topic, payload = GESTURE_ACTIONS[erkannte_geste]
                mqtt_client.publish(topic, payload)
                print(f"Geste erkannt: {erkannte_geste} -> {topic}: {payload}")

                last_sent_gesture = erkannte_geste
                last_sent_time = jetzt
        elif erkannte_geste is None:
            # Wenn kurz keine Hand im Bild ist, Cooldown zuruecksetzen,
            # damit dieselbe Geste beim naechsten Zeigen sofort wieder sendet
            last_sent_gesture = None

        cv2.imshow("Smart Home Gestensteuerung", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    mqtt_client.loop_stop()
    mqtt_client.disconnect()


if __name__ == "__main__":
    main()