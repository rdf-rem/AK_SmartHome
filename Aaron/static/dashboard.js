// ------------------------------
// Dashboard.js
// ------------------------------

const gestureMap = {
    "Open_Palm": "Offene Hand",
    "Closed_Fist": "Geschlossene Faust",
    "Thumb_Up": "Daumen hoch",
    "Thumb_Down": "Daumen runter",
    "Victory": "Victory",
    "-": "—",
    "None": "—"
};


// ------------------------------
// Uhr aktualisieren
// ------------------------------

function updateClock(){

    const now = new Date();

    document.getElementById("clock").textContent =
        now.toLocaleTimeString("de-DE");

}


// ------------------------------
// Animation beim Aktualisieren
// ------------------------------

function animateUpdate(element){

    element.style.opacity = "0.4";
    element.style.transform = "scale(0.98)";

    setTimeout(() => {

        element.style.opacity = "1";
        element.style.transform = "scale(1)";

    },150);

}


// ------------------------------
// Dashboard aktualisieren
// ------------------------------

async function updateDashboard(){

    try{

        const response = await fetch("/state");

        const state = await response.json();


        // Licht

        const light = document.getElementById("light");

        light.textContent = state.light ? "EIN" : "AUS";

        light.className = state.light
            ? "card-value on"
            : "card-value off";

        animateUpdate(light);


        // Rollo

        const blinds = document.getElementById("blinds");

        blinds.textContent = state.blinds
            ? "GEÖFFNET"
            : "GESCHLOSSEN";

        blinds.className = state.blinds
            ? "card-value on"
            : "card-value off";

        animateUpdate(blinds);


        // Temperatur

        const temperature = document.getElementById("temperature");

        temperature.textContent = state.temperature;

        animateUpdate(temperature);


        // Bewegung

        const motion = document.getElementById("motion");

        motion.textContent = state.motion
            ? "ERKANNT"
            : "KEINE";

        motion.className = state.motion
            ? "card-value on"
            : "card-value off";

        animateUpdate(motion);


        // Geste

        const gesture = document.getElementById("gestureText");

        gesture.textContent =
            gestureMap[state.last_gesture] || state.last_gesture;

        animateUpdate(gesture);

    }

    catch(error){

        console.log("Dashboard konnte nicht aktualisiert werden.");

    }

}


// ------------------------------
// Start
// ------------------------------

updateClock();

updateDashboard();

setInterval(updateClock,1000);

setInterval(updateDashboard,2000);