// Initialize socket connection to server
const socket = io("http://192.168.8.160:5000"); 

const videoElement = document.getElementById("videoElement");
const canvasElement = document.getElementById("canvasElement");
const ctx = canvasElement.getContext("2d");

// Setting up MediaPipe for hand tracking
const hands = new Hands({
    locateFile: (file) => {
        return `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`;
    }
});

// MediaPipe hands model config
hands.setOptions({
    maxNumHands: 1,
    modelComplexity: 1,
    minDetectionConfidence: 0.5,
    minTrackingConfidence: 0.6
});

// Function to process hand tracking results
hands.onResults((results) => {
    ctx.clearRect(0, 0, canvasElement.width, canvasElement.height);


    ctx.save();
    ctx.translate(canvasElement.width, 0);
    ctx.scale(-1, 1);

    // drawing mediapipe landmarks in canvas
    if (results.multiHandLandmarks) {
        results.multiHandLandmarks.forEach((landmarks) => {
            landmarks.forEach((lm) => {
                const x = lm.x * canvasElement.width;
                const y = lm.y * canvasElement.height;

                ctx.beginPath();
                ctx.arc(x, y, 5, 0, 2 * Math.PI);
                ctx.fillStyle = "red";
                ctx.fill();
            });
        });

        // Send landmarks to the server
        sendLandmarks(results.multiHandLandmarks);
    }

    ctx.restore();
});

// Start the webcam and begin MediaPipe processing
async function startCamera() {
    const stream = await navigator.mediaDevices.getUserMedia({ video: { width: 640, height: 480 } });
    videoElement.srcObject = stream;

    const camera = new Camera(videoElement, {
        onFrame: async () => {
            await hands.send({ image: videoElement });
        },
        width: 640,
        height: 480
    });
    camera.start();
}

// Start camera
startCamera();

// Send the captured landmarks to the Flask server in JSON format
function sendLandmarks(landmarks) {
    const handData = landmarks.map(hand => hand.map(lm => [lm.x, lm.y, lm.z]));
    socket.emit("hand_landmarks", { hands: handData });
}

// Listen for the landmarks from the server
socket.on("hand_landmarks", (data) => {
    console.log("Received data:", data);

    // Get the elements where we will display data
    const rawLandmarksBox = document.getElementById("rawLandmarks");
    const normalizedLandmarksBox = document.getElementById("normLandmarks");
    const anglesBox = document.getElementById("angles");

    if (!data.original_landmarks || data.original_landmarks.length === 0) {
        rawLandmarksBox.innerHTML = "<strong>No hand detected</strong>";
        normalizedLandmarksBox.innerHTML = "<strong>No hand detected</strong>";
        anglesBox.innerHTML = "<strong>No hand detected</strong>";
        return;
    }

    let rawLandmarksHTML = "<strong>Raw Landmarks:</strong><br>";
    let normLandmarksHTML = "<strong>Normalized Landmarks:</strong><br>";
    let anglesHTML = "<strong>Angles:</strong><br>";

    data.angles.forEach((angle, index) => {
        anglesHTML += `Angle ${index + 1}: ${angle.toFixed(2)}°<br>`;
    });

    data.normalized_landmarks.forEach((landmark, index) => {
        normLandmarksHTML += `Point ${index}: X=${landmark[0].toFixed(3)}, Y=${landmark[1].toFixed(3)}, Z=${landmark[2].toFixed(3)}<br>`;
    });

    data.original_landmarks.forEach((landmark, index) => {
        rawLandmarksHTML += `Point ${index}: X=${landmark[0].toFixed(3)}, Y=${landmark[1].toFixed(3)}, Z=${landmark[2].toFixed(3)}<br>`;
    });

    // Update the HTML elements with the formatted data
    rawLandmarksBox.innerHTML = rawLandmarksHTML;
    normalizedLandmarksBox.innerHTML = normLandmarksHTML;
    anglesBox.innerHTML = anglesHTML;
});


