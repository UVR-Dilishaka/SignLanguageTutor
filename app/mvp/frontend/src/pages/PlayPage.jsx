import React, { use, useEffect, useRef, useState } from "react";
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
  const [prediction, setPrediction] = useState(null);
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [handData, setHandData] = useState([]);
  const [notDetectingHands, setNotDetectingHands] = useState(true);
  const [tooFar, setTooFar] = useState(false);
  const [language, setLanguage] = useState("Sinhala");
  const [userData, setUserData] = useState(null);
  const [signs, setSigns] = useState([]);
  const [currentSign, setCurrentSign] = useState(null);
  const [timer, setTimer] = useState(10);
  const [correctPredictions, setCorrectPredictions] = useState(0);
  const [won, setWon] = useState(false);
  const [showGoodJob, setShowGoodJob] = useState(false);
  const [showTryAgain, setShowTryAgain] = useState(false);
  const [correctSigns, setCorrectSigns] = useState([]);
  const [incorrectSigns, setIncorrectSigns] = useState([]);
  const [showPopup, setShowPopup] = useState(false);
  const [hintUsed, setHintUsed] = useState(false);



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
      // console.log(data);
    }
  };

  const loadSigns = async () => {
    if (userData) {
      const signsData = await fetchSigns(userData.id, language, navigate);
      if (signsData) {
        setSigns(signsData.selected_signs);
        if (signsData.selected_signs.length > 0) {
          setCurrentSign(signsData.selected_signs[0]);

        }
      }
    }
  }

  const handleNextRound = () => {
    setShowPopup(true);
  };

  const handleShowHint = () => {
    setHintUsed(true);
  };
  

  useEffect(() => {
    let interval;
    if (isPlaying) {
      setTimer(10);
      setShowGoodJob(false);
      setShowTryAgain(false) // Reset message

      interval = setInterval(() => {
        setTimer((prev) => {
          if (prev <= 1 || won) {
            clearInterval(interval);
            setIsPlaying(false);
            setCorrectPredictions(0);
            setPrediction(null);
            


            if (won) {
              setShowGoodJob(true);
              setWon(false);
              setCorrectSigns((prevSigns) => [...prevSigns, currentSign]);
              

            }else{
              setShowTryAgain(true);
              setIncorrectSigns((prevSigns) => [...prevSigns, currentSign]);
              
            }

            // const currentSignIndex = signs.indexOf(currentSign);
            // const nextSignIndex = (currentSignIndex + 1) % signs.length;
            // setCurrentSign(signs[nextSignIndex]);
            setHintUsed(false);
            const currentSignIndex = signs.indexOf(currentSign);
            const nextSignIndex = (currentSignIndex + 1);

            // Check if the current sign is the last one
            if (nextSignIndex >= signs.length) {
              handleNextRound(); // Trigger the next round
            } else {
              setCurrentSign(signs[nextSignIndex]); // Go to the next sign
            }



            return 0;
          }
          return prev - 1;
        });
      }, 1000);

      
    } else {
      clearInterval(interval);
    }

    return () => clearInterval(interval);
  }, [isPlaying, won]);

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


  // hook for hand detection and prediction
  useEffect(() => {
    const videoElement = videoRef.current;
    const canvasElement = canvasRef.current;
    const ctx = canvasElement.getContext("2d");

    if (!isPlaying) {
      setPrediction(null);
    }
  
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
  
        
        processHandData(results.multiHandLandmarks);
        
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
          ctx.fillStyle = "purple";
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
      // only send hand landmarks when play is on
      if (!isTooFar && isPlaying) {
        
        try {
          const response = await fetch("http://127.0.0.1:5000/poseEstimation/hand_landmarks", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ language:language, hands: handPoints }),
            
          });

          const result = await response.json();


          if(isPlaying) setPrediction(result.prediction);{
            // console.log(result.prediction);
            console.log("Current sign:", currentSign);
            console.log("Predicted sign:", result.prediction);

          let predictedsign = result.prediction

          if (language === "Sinhala") {
            predictedsign = predictedsign + 12
          }
          

          if (predictedsign === currentSign) {
            setCorrectPredictions((prev) => {
              const newCorrectPredictions = prev + 1;
              console.log("Correct matches:", newCorrectPredictions);

              if (newCorrectPredictions >= 50) {
                setWon(true); // Set to true when predictions reach 100
              }

              return newCorrectPredictions;
            });
          }
          }
          
          


          
          
          
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
  }, [isPlaying,language,currentSign]);



 

  return (
    <div className="game-container">
      <PlayHeader />
      <div className="main">

        <div className="left-section">


          <div className="camerafeed">
          <video ref={videoRef} className="video-feed" width="640" height="480" autoPlay />
          <canvas ref={canvasRef} width="640" height="480" className="canvas-overlay" />
          </div>

          <div className="metric-dash">
            <div className="status">
              {notDetectingHands ? (
                <p className="error">I cant see any hands</p>
              ) : tooFar ? (
                <p className="warning">Bring your hand closer</p>
              ) : (
                <p className="success">You are good to go</p>
              )}
            </div>
            {isPlaying && (
            <div className="prediction-container">
              <p className="prediction-text">
              Your letter is:{" "}
              {prediction 
                ? (Object.keys(letterdic).find(key => letterdic[key] === (language.toLowerCase() === "sinhala" ? prediction + 12 : prediction)) || "?") 
                : "..."}
              </p>
            </div>
            )}

            {(isPlaying || showGoodJob || showTryAgain)&&(
            <div className="timer">
              {showGoodJob ? (
                <p className="success">Nice! Try the next sign</p>
              ) : showTryAgain ? (
                <p className="warning">Keep going! Try the Next sign.</p>
              ) : isPlaying ? (
                <p>Time left: {timer}s</p>
              ) : null}
            </div>
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
            {signs.map((sign, index) => {
              const isCorrect = correctSigns.includes(sign);
              const isIncorrect = incorrectSigns.includes(sign);

              let signColor;
              if (isCorrect) {
                signColor = "green"; // Green for correct
              } else if (isIncorrect) {
                signColor = "red"; // Red for incorrect
              } else {
                signColor = sign === currentSign ? "darkblue" : "lightblue"; // Default color
              }

              return (
                <LetterCard
                  key={index}
                  text={Object.keys(letterdic).find(key => letterdic[key] === sign) || "?"}
                  color={signColor} // Assign color based on correctness
                />
              );
            })}
          </div>
          <div className="hint-button-container">
          <button className="btn" onClick={handleShowHint}>
            Show Hint
          </button>
          </div>
          
          <div className="hint-img-container">
          <img 
            src={`/images/${hintUsed ? `${currentSign}_hint` : currentSign}.jpg`}
            alt="Sign hint" 
            className="hint-image"
          />
          </div>

        </div>
      </div>


        {showPopup && (
          <div className="popup-overlay">
            <div className="popup">
              <h2>Round Summary</h2>
              <p><strong>Correct Signs:</strong> {correctSigns.join(", ") || "None"}</p>
              <p><strong>Incorrect Signs:</strong> {incorrectSigns.join(", ") || "None"}</p>
              <button onClick={() => {
                
                setShowPopup(false); 
                setCorrectSigns([]);
                setIncorrectSigns([]);
                loadSigns()
                setCurrentSign(signs[0]);
              }}>
                Next Round
              </button>
            </div>
          </div>
        )}
      <Footer />
    </div>
  );
};

export default PlayPage;
