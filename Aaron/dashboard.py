"""
dashboard.py

Web-Dashboard für das Smart-Home-System.

Autor: Aaron
Unterstützung: ChatGPT
Projekt: Smart Home Steuerung mittels Gestenerkennung
"""

import json
from pathlib import Path

from flask import Flask, jsonify, render_template

app = Flask(__name__)

STATE_FILE = Path("data/state.json")


def load_state():
    """Lädt den aktuellen Zustand des Smart Homes."""

    if STATE_FILE.exists():

        with open(STATE_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    # Standardwerte beim ersten Start
    return {
        "light": False,
        "blinds": False,
        "temperature": 0.0,
        "motion": False,
        "last_gesture": "-"
    }


@app.route("/")
def index():
    """Startseite des Dashboards."""

    return render_template(
        "index.html",
        state=load_state()
    )


@app.route("/state")
def state():
    """Liefert den aktuellen Zustand als JSON."""

    return jsonify(load_state())


if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )