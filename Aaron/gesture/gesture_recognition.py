import cv2
import mediapipe as mp

print("MediaPipe-Version:", mp.__version__)

# -----------------------------
# MediaPipe konfigurieren
# -----------------------------
BaseOptions = mp.tasks.BaseOptions
VisionRunningMode = mp.tasks.vision.RunningMode

GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizer

options = mp.tasks.vision.GestureRecognizerOptions(
    base_options=BaseOptions(
        model_asset_path="models/gesture_recognizer.task"
    ),
    running_mode=VisionRunningMode.IMAGE
)

recognizer = GestureRecognizer.create_from_options(options)

print("✅ Modell geladen")

# -----------------------------
# Webcam starten
# -----------------------------
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Webcam konnte nicht geöffnet werden.")
    exit()

print("✅ Webcam gestartet")
print("Drücke q zum Beenden")

# Damit dieselbe Geste nicht 30-mal pro Sekunde ausgegeben wird
last_gesture = ""

# -----------------------------
# Hauptschleife
# -----------------------------
while True:

    ret, frame = cap.read()

    if not ret:
        break

    frame = cv2.flip(frame, 1)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb
    )

    result = recognizer.recognize(mp_image)

    if result.gestures:

        gesture = result.gestures[0][0].category_name

        if gesture != last_gesture:
            print("👉", gesture)
            last_gesture = gesture

        cv2.putText(
            frame,
            gesture,
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0,255,0),
            2
        )

    cv2.imshow("Gesture Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()