import React, { useEffect, useRef, useState } from "react";
import { Hands } from "@mediapipe/hands";
import { Camera } from "@mediapipe/camera_utils";
import { useNavigate } from "react-router-dom";
import { fetchUserData } from "../util/fetchuser";
import { fetchSigns } from "../util/fetchnextsigns";
import PlayHeader from "../components/PlayHeader";
import Footer from "../components/Footer";
import LetterCard from "../components/LetterCard";
import "../game.css";

const PlayPage = () => {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [handData, setHandData] = useState([]);
  const [notDetectingHands, setNotDetectingHands] = useState(true);
  const [tooFar, setTooFar] = useState(false);
  const [language, setLanguage] = useState("Sinhala");
  const [userData, setUserData] = useState(null);
  const [signs, setSigns] = useState([]);
  const navigate = useNavigate();
  const letterdic = {
    "அ": 1, "ஆ": 2, "இ": 3, "ஈ": 4, "உ": 5, "ஊ": 6, "எ": 7, "ஏ": 8, "ஒ": 9, "ஓ": 10, "ஐ": 11, "ஔ": 12,
    "අ": 13, "ආ": 14, "ඇ": 15, "ඉ": 16, "උ": 17, "එ": 18, "ග": 19, "ව": 20, "ඩ": 21, "ද": 22, "ය": 23, "හ": 24
  };

  const [isPlaying, setIsPlaying] = useState(false);
  const togglePlay = () => {
    setIsPlaying((prev) => !prev);
  };

  const loadUserData = async () => {
    const data = await fetchUserData(navigate);
    if (data) {
      setUserData(data);
      console.log(data);
    }
  };

  const loadSigns = async () => {
    if (userData) {
      const signsData = await fetchSigns(userData.id, language, navigate);
      if (signsData) {
        setSigns(signsData.selected_signs);
      }
    }
  }


  // this hook will load signs if new userdata is loaded or if the language is changed
  useEffect(() => {
    if (userData) {
      loadSigns();
    }
  }, [userData, language]);


  // hook for loading user data
  useEffect(() => {
    loadUserData();
  }, [navigate]);

  


  // hook for hand detection
  useEffect(() => {
    const videoElement = videoRef.current;
    const canvasElement = canvasRef.current;
    const ctx = canvasElement.getContext("2d");
  
    const hands = new Hands({
      locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`,
    });
  
    hands.setOptions({
      maxNumHands: 1,
      modelComplexity: 1,
      minDetectionConfidence: 0.7,
      minTrackingConfidence: 0.7,
    });
  
    hands.onResults(handleHandResults);
  
    async function startCamera() {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: { width: 640, height: 480 } });
        videoElement.srcObject = stream;
        const camera = new Camera(videoElement, {
          onFrame: async () => await hands.send({ image: videoElement }),
          width: 640,
          height: 480,
        });
        camera.start();
      } catch (error) {
        console.error("Error accessing camera:", error);
      }
    }
  
    function handleHandResults(results) {
      ctx.clearRect(0, 0, canvasElement.width, canvasElement.height);
  
      if (results.multiHandLandmarks?.length) {
        setNotDetectingHands(false);
        drawHandLandmarks(ctx, results.multiHandLandmarks);
  
        // Only process hand data when Play is ON
        if (isPlaying) {
          processHandData(results.multiHandLandmarks);
        }
      } else {
        setNotDetectingHands(true);
      }
    }
  
    function drawHandLandmarks(ctx, landmarks) {
      landmarks.forEach((hand) => {
        hand.forEach((lm) => {
          const x = (1 - lm.x) * canvasElement.width;
          const y = lm.y * canvasElement.height;
          ctx.beginPath();
          ctx.arc(x, y, 5, 0, 2 * Math.PI);
          ctx.fillStyle = "lime";
          ctx.fill();
        });
      });
    }
  
    async function processHandData(landmarks) {
      const handPoints = landmarks.map((hand) => hand.map((lm) => [lm.x, lm.y, lm.z]));
      setHandData(handPoints);
  
      const wrist = handPoints[0][0];
      const middleMCP = handPoints[0][9];
      const indexMCP = handPoints[0][5];
      const pinkyMCP = handPoints[0][17];
  
      const refDistance1 = calculateDistance(wrist, middleMCP);
      const refDistance2 = calculateDistance(indexMCP, pinkyMCP);
  
      const isTooFar = refDistance1 < 0.25 || refDistance2 < 0.10;
      setTooFar(isTooFar);
  
      if (!isTooFar) {
        try {
          await fetch("http://127.0.0.1:5000/poseEstimation/hand_landmarks", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ hands: handPoints }),
          });
        } catch (error) {
          console.error("Error sending hand landmarks:", error);
        }
      }
    }
  
    function calculateDistance(point1, point2) {
      return Math.sqrt(
        (point1[0] - point2[0]) ** 2 +
        (point1[1] - point2[1]) ** 2 +
        (point1[2] - point2[2]) ** 2
      );
    }
  
    startCamera();
  
    return () => {
      hands.close();
      videoElement?.srcObject?.getTracks().forEach((track) => track.stop());
    };
  }, [isPlaying]);



  
  return (
    <div className="game-container">
      <PlayHeader />
      <div className="main">
        <div className="left-section">
          <video ref={videoRef} className="video-feed" width="640" height="480" autoPlay />
          <canvas ref={canvasRef} width="640" height="480" className="canvas-overlay" />
          <div className="status">
            {notDetectingHands ? (
              <p className="error">No hands detected</p>
            ) : tooFar ? (
              <p className="warning">Hand is too far</p>
            ) : (
              <p className="success">Hand position is good</p>
            )}
          </div>
        </div>

        <div className="right-section">
          <div className="button-container">
            <button className="btn" onClick={() => navigate("/profile")}>Profile</button>
            <button className="btn" onClick={togglePlay}>
            {isPlaying ? "Pause" : "Play"}
            </button>
          </div>
          <select className="dropdown" value={language} onChange={(e) => setLanguage(e.target.value)}>
            <option value="Sinhala">Sinhala</option>
            <option value="Tamil">Tamil</option>
          </select>
          <div className="letter-container">
          {signs.map((sign, index) => (
              <LetterCard key={index} text={Object.keys(letterdic).find(key => letterdic[key] === sign) || "?"} color="lightblue" />
         ))}
          </div>
        </div>
      </div>
      <Footer />
    </div>
  );
};

export default PlayPage;
