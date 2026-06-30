"""
config.py

Lädt die Konfiguration aus der Datei config.json.

Autor: Aaron (ChatGPT)
Projekt: Smart Home Steuerung mittels Gestenerkennung
"""

import json


class Config:
    """Liest die Konfiguration aus der Datei config.json."""

    def __init__(self, filename="config.json"):

        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)

        # Kamera
        self.camera_index = data["camera"].get("index", 0)
        self.camera_flip = data["camera"].get("flip", True)
        self.show_fps = data["camera"].get("show_fps", False)
        self.display_landmarks = data["camera"].get("display_landmarks", True)

        # MediaPipe
        self.model_path = data["mediapipe"].get(
            "model",
            "models/gesture_recognizer.task"
        )

        self.detection_confidence = data["mediapipe"].get(
            "detection_confidence",
            0.7
        )

        self.tracking_confidence = data["mediapipe"].get(
            "tracking_confidence",
            0.5
        )

        self.max_num_hands = data["mediapipe"].get(
            "max_num_hands",
            2
        )

        # MQTT
        self.mqtt_broker = data["mqtt"].get("broker", "localhost")
        self.mqtt_port = data["mqtt"].get("port", 1883)
        self.gesture_topic = data["mqtt"].get(
            "gesture_topic",
            "gesture"
        )
        self.debug_topic = data["mqtt"].get(
            "debug_topic",
            "debug"
        )

        # Gestenerkennung
        self.cooldown = data["gesture_recognition"].get(
            "cooldown_seconds",
            0.5
        )