"""
camera.py

Verwaltet den Zugriff auf die Webcam.

Autor: Aaron
Projekt: Smart Home Steuerung mittels Gestenerkennung
"""

import cv2


class Camera:
    """Stellt Bilder der Webcam bereit."""

    def __init__(self, camera_index=0, flip=True):
        self.flip = flip
        self.cap = cv2.VideoCapture(camera_index)

        if not self.cap.isOpened():
            raise RuntimeError("Webcam konnte nicht geöffnet werden.")

    def read(self):
        success, frame = self.cap.read()

        if not success:
            return None

        if self.flip:
            frame = cv2.flip(frame, 1)

        return frame

    def release(self):
        self.cap.release()