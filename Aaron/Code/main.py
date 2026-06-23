import argparse
import time
from collections import deque

import cv2
import mediapipe as mp
import paho.mqtt.client as mqtt


DEFAULT_BROKER = "broker.hivemq.com"
DEFAULT_PORT = 1883
DEFAULT_TOPIC_GESTURE = "home/gesture"
DEFAULT_TOPIC_LIGHT = "home/livingroom/light"
DEFAULT_TOPIC_BLINDS = "home/livingroom/blinds"


class MqttPublisher:
    def __init__(self, broker: str, port: int = DEFAULT_PORT):
        self.broker = broker
        self.port = port
        self.client = mqtt.Client()
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.connected = False

    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.connected = True
            print(f"MQTT connected to {self.broker}:{self.port}")
        else:
            print(f"MQTT connection failed with code {rc}")

    def _on_disconnect(self, client, userdata, rc):
        self.connected = False
        print("MQTT disconnected")

    def connect(self):
        self.client.connect(self.broker, self.port, keepalive=60)
        self.client.loop_start()
        timeout = time.time() + 5
        while not self.connected and time.time() < timeout:
            time.sleep(0.1)

    def publish(self, topic: str, payload: str):
        if not self.connected:
            print("MQTT client not connected, cannot publish")
            return
        self.client.publish(topic, payload)
        print(f"Published {payload!r} to topic {topic}")

    def stop(self):
        self.client.loop_stop()
        self.client.disconnect()


class GestureClassifier:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=1,
            model_complexity=1,
            min_detection_confidence=0.6,
            min_tracking_confidence=0.6,
        )
        self.mp_draw = mp.solutions.drawing_utils

    def classify(self, image):
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        result = self.hands.process(rgb)
        if not result.multi_hand_landmarks:
            return None, image

        hand_landmarks = result.multi_hand_landmarks[0]
        self.mp_draw.draw_landmarks(image, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
        gesture = self._classify_from_landmarks(hand_landmarks, image.shape)
        return gesture, image

    def _classify_from_landmarks(self, landmarks, image_shape):
        width, height = image_shape[1], image_shape[0]
        coords = [(lm.x * width, lm.y * height) for lm in landmarks.landmark]

        finger_states = []
        tips = [4, 8, 12, 16, 20]
        pip_joints = [2, 6, 10, 14, 18]

        for tip_index, pip_index in zip(tips, pip_joints):
            tip_x, tip_y = coords[tip_index]
            pip_x, pip_y = coords[pip_index]
            if tip_index == 4:
                # Thumb uses x orientation on the right hand, reversed for left hand.
                finger_states.append(tip_x < pip_x)
            else:
                finger_states.append(tip_y < pip_y)

        count = sum(finger_states)

        if count == 0:
            return "fist"
        if count == 5:
            return "open_palm"
        if finger_states[1] and finger_states[2] and not finger_states[3] and not finger_states[4]:
            return "peace"
        if count == 3 and finger_states[1] and finger_states[2] and finger_states[3]:
            return "three_fingers"
        return None


def build_message(gesture: str):
    if gesture == "open_palm":
        return {
            "gesture": "open_palm",
            "actions": [
                (DEFAULT_TOPIC_GESTURE, "open_palm"),
                (DEFAULT_TOPIC_LIGHT, "ON"),
            ],
        }
    if gesture == "fist":
        return {
            "gesture": "fist",
            "actions": [
                (DEFAULT_TOPIC_GESTURE, "fist"),
                (DEFAULT_TOPIC_LIGHT, "OFF"),
            ],
        }
    if gesture == "peace":
        return {
            "gesture": "peace",
            "actions": [
                (DEFAULT_TOPIC_GESTURE, "peace"),
                (DEFAULT_TOPIC_BLINDS, "OPEN"),
            ],
        }
    if gesture == "three_fingers":
        return {
            "gesture": "three_fingers",
            "actions": [
                (DEFAULT_TOPIC_GESTURE, "three_fingers"),
                (DEFAULT_TOPIC_BLINDS, "CLOSED"),
            ],
        }
    return None


def main():
    parser = argparse.ArgumentParser(description="MediaPipe gesture publisher for Smart Home MQTT")
    parser.add_argument("--broker", default=DEFAULT_BROKER, help="MQTT broker hostname")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help="MQTT broker port")
    parser.add_argument("--camera", type=int, default=0, help="Camera device index")
    args = parser.parse_args()

    mqtt_publisher = MqttPublisher(args.broker, args.port)
    mqtt_publisher.connect()

    classifier = GestureClassifier()
    recent_gestures = deque(maxlen=10)
    last_published = None
    last_publish_time = 0

    capture = cv2.VideoCapture(args.camera)
    if not capture.isOpened():
        print(f"Unable to open camera {args.camera}")
        return

    print("Starting camera. Press ESC to quit.")
    while True:
        ret, frame = capture.read()
        if not ret:
            break

        gesture, annotated_frame = classifier.classify(frame)
        if gesture:
            recent_gestures.append(gesture)
            most_common = max(set(recent_gestures), key=recent_gestures.count)
            if most_common == gesture:
                now = time.time()
                if gesture != last_published or now - last_publish_time > 1.5:
                    message = build_message(gesture)
                    if message:
                        for topic, payload in message["actions"]:
                            mqtt_publisher.publish(topic, payload)
                        last_published = gesture
                        last_publish_time = now

        if gesture:
            cv2.putText(
                annotated_frame,
                f"Gesture: {gesture}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2,
                cv2.LINE_AA,
            )
        else:
            cv2.putText(
                annotated_frame,
                "No gesture detected",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 255),
                2,
                cv2.LINE_AA,
            )

        cv2.putText(
            annotated_frame,
            "Open palm=Light ON, Fist=Light OFF, Peace=Blinds OPEN, 3 fingers=Blinds CLOSED",
            (10, annotated_frame.shape[0] - 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 255),
            1,
            cv2.LINE_AA,
        )

        cv2.imshow("Smart Home Gesture MQTT", annotated_frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    capture.release()
    cv2.destroyAllWindows()
    mqtt_publisher.stop()


if __name__ == "__main__":
    main()

