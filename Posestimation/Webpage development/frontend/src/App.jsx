import BlurOverlay from './BlurOverlay.jsx';
import Canvas from './Canvas.jsx';
import Greeting from './Greeting.jsx';
import Header from './Header.jsx'
import Hint from './Hint.jsx';
import HomeButton from './HomeButton.jsx';
import HomeButton1 from './HomeButton1.jsx';
import LetterSwitch from './LetterSwitch.jsx';
import LevelLetters from './LevelLetters.jsx';
import LevelNo from './LevelNo.jsx';
import LevelSelection from './LevelSelection.jsx';
import Notification from './Notification.jsx';
import Score from './score.jsx';
import StartButton from './StartButton.jsx';
import StartCountdown from './StartCountdown.jsx';
import StartNote from './StartNote.jsx';
import Timer from './Timer.jsx';

import { useState } from "react";
import { useEffect, useRef } from "react";
import { io } from "socket.io-client"; 
import axios from "axios";

// Importing MediaPipe hands package
import * as handsModule from "@mediapipe/hands";
import { Camera } from "@mediapipe/camera_utils";

// Connecting to the backend WebSocket server
const socket = io("http://127.0.0.1:5000");

function App() {

    const [message, setMessage] = useState("");

    useEffect(() => {
        axios.get("http://127.0.0.1:5000/api/hello")
            .then(response => {
                setMessage(response.data.message);
            })
            .catch(error => {
                console.error("Error fetching data:", error);
            });
    }, []);


    const [initialPage, setInitialPage] = useState(true);
    const [username, setUsername] = useState("Guest");
    const [currentLevel, setCurrentLevel] = useState(1);
    const [currentLetters, setCurrentLetters] = useState([]);
    const [unlockedLevels, setUnlockedLevels] = useState([1,2,4])
    const [completedLetters, setCompletedLetters] = useState(["A"]);
    const [selectedLetter, setSelectedLetter] = useState('')
    const [score, setScore] = useState(0)
    const [countdownTime, setCountdownTime] = useState(5);
    let allLetters = ['A','B','C','D','E',"F","G","H","I",'J','K','L','M','N','O']
    const [hintUsage, setHintUsage] = useState([]);
    

    const handleStartClick = () => {
        setInitialPage(false);  // Hide the welcome-screen when start button is clicked
    };

    const goToHome = () => {
        window.location.href = 'https://www.google.com';
    }

    // Shows a lock sign in locked levels
    const lockinglevels = () => {
        unlockedLevels.forEach(level => {
            const levelBlock = document.getElementById(`lvl${level}`);
            if (levelBlock) {
                levelBlock.innerText = `${level}`;
                levelBlock.classList.add("unlocked-level");
            }
        });
    };

    useEffect(() => {
        lockinglevels(); //Automatic level updating
    }, [unlockedLevels]);

    // Handles level selecting in the welcome screen
    const handleLevelClick = (level) => {
        if (unlockedLevels.includes(level)) {
            setCurrentLevel(level); 
    
            // Update the inner HTML of level-container1 p
            const levelText = document.querySelector(".level-container1 p");
            if (levelText) {
                levelText.innerHTML = `Selected Level: ${level}`;
            }
    
            // Remove zoom effect from all level boxes
            document.querySelectorAll(".level-select").forEach((box) => {
                box.classList.remove("selected-level");
            });
    
            // Apply zoom effect to the clicked level box
            document.getElementById(`lvl${level}`).classList.add("selected-level");
            // document.querySelector("")
        }
    };

    // For marking completed, uncompleted and selected letters in the letter display
    const letterStatusDisplay = () => {
        currentLetters.forEach((letter, index) => {
            const letterBox = document.getElementById(`letter-box${index + 1}`);
            if (letterBox) {
                letterBox.innerHTML = `<p>${letter}</p>`; 

                // Reset styles
                letterBox.classList.remove("completed", "selected");

                // Apply styles based on conditions
                if (completedLetters.includes(letter)) {
                    letterBox.classList.add("completed");
                }
                if (letter === selectedLetter) {
                    letterBox.classList.add("selected");
                }
            }
        });
    };
    
    // Update letter-box styles when dependencies change
    useEffect(() => {
        letterStatusDisplay();
    }, [currentLetters, completedLetters, selectedLetter]);

    // Game initial stage function
    const initialMoment = () =>{
        const startNote = document.querySelector(".start-note")
        const timer = document.querySelector(".timer")
        const countdown = document.querySelector(".start-countdown")

        startNote.style.display = "block"
        timer.style.display = "none"
        countdown.style.display = "none"
    }

    // Taking first letter of the current letters as the selected letter initially
    useEffect(() => {
        if (currentLetters.length > 0) {
            setSelectedLetter(currentLetters[0]);  
        }
    }, [currentLetters]);


    // Handle current letter after clicking
    const handleLetterClick = (letter) =>{
        setSelectedLetter(letter)

        const startNoteDiv = document.querySelector('.start-note');
        startNoteDiv.classList.add('start-note-effect')
        
        // Remove the class after the transition ends to reset the scale
        startNoteDiv.addEventListener('transitionend', () => {
            startNoteDiv.classList.remove('start-note-effect');
        });
        initialMoment()
    }


    //Handle after clicking start in game window
    const handleGameStartClick = () => {
        setCountdownTime(5); 
        const startNote = document.querySelector(".start-note");
        const countdown = document.querySelector(".start-countdown");
    
        if (startNote) startNote.style.display = "none"; 
        if (countdown) countdown.style.display = "block"; 
    
        // Start the countdown
        const timer = setInterval(() => {
            setCountdownTime(prevTime => {
                if (prevTime <= 1) {
                    clearInterval(timer);
                    if (countdown) countdown.style.display = "none";
                    return 0;
                }
                return prevTime - 1;
            });
        }, 1000);

        //After timer, run the game


        //If detected update score and go to initial moment
    };
    
    // Decide whether to show or not the hint based on previous usage of hint for that particular letter 
    const hintDisplay = () => {
        const letterIndex = allLetters.indexOf(selectedLetter)
        const hintUsed = hintUsage[letterIndex]

        const hintBox = document.querySelector('.hint-box');
        const hintButton = document.querySelector('.hint-button');

        if (hintUsed) {
            // If hint is used, display the hint box and hide the hint button
            if (hintBox) hintBox.style.display = 'block';
            if (hintButton) hintButton.style.display = 'none';
        } else {
            // If hint is not used, display the hint button and hide the hint box
            if (hintBox) hintBox.style.display = 'none';
            if (hintButton) hintButton.style.display = 'block';
        }
    };
    
    useEffect(() => {
        hintDisplay(); 
    }, [selectedLetter, hintUsage]);

    // Handling hint buttton click
    const handleHintButtonClick = () => {
        const hintUsedLetterIndex = allLetters.indexOf(selectedLetter);
        
        // Create a new array to avoid mutating state directly
        const updatedHintUsage = [...hintUsage];
        updatedHintUsage[hintUsedLetterIndex] = true;
    
        setHintUsage(updatedHintUsage);
        console.log(hintUsage);
    };

    //Handling letter switch button displaying
    useEffect(() => {
        const currentIndex = currentLetters.indexOf(selectedLetter);
        const prevButton = document.querySelector(".previous-letter-switch");
        const nextButton = document.querySelector(".next-letter-switch");
    
        if (prevButton) {
            if (currentIndex === 0) {
                prevButton.style.display = "none";
            } else {
                prevButton.style.display = "block";
            }
        }
    
        if (nextButton) {
            if (currentIndex === currentLetters.length - 1) {
                nextButton.style.display = "none";
            } else {
                nextButton.style.display = "block";
            }
        }
    }, [selectedLetter]);

    //Handling next letter button click
    const handleNextLetterButtonClick = () => {
        const nextLetter = currentLetters[currentLetters.indexOf(selectedLetter) + 1]
        setSelectedLetter(nextLetter)
    }

    //Handling previous letter button click
    const handlePreviousLetterButtonClick = () => {
        const prevLetter = currentLetters[currentLetters.indexOf(selectedLetter) - 1]
        setSelectedLetter(prevLetter)
    }


    //Requesting username
    useEffect(() => {
        // Make a GET request to Flask to fetch the username
        axios.get("http://127.0.0.1:5000/api/username")
            .then(response => {
                setUsername(response.data.username); // Set username from the response
            })
            .catch(error => {
                console.error("Error fetching username:", error);
            });
    }, []); // Empty dependency array ensures this runs once after component mounts


     // Fetch initial level and letters when the app loads
     useEffect(() => {
        axios.get("http://127.0.0.1:5000/api/get_current_level")
            .then(response => {
                setCurrentLevel(response.data.level);
                setCurrentLetters(response.data.assigned_letters);
            })
            .catch(error => console.error("Error fetching level:", error));
    }, []);

    // Listen for level updates from Flask
    useEffect(() => {
        socket.on('level_updated', (data) => {
            setCurrentLevel(data.level);
            setCurrentLetters(data.assigned_letters);
        });

        return () => {
            socket.off('level_updated');
        };
    }, []);

    // Fetch initial score from Flask
    useEffect(() => {
        axios.get("http://127.0.0.1:5000/api/get_score")
            .then(response => setScore(response.data.score))
            .catch(error => console.error("Error fetching score:", error));
    }, []);

    // Listen for real-time score updates from Flask
    useEffect(() => {
        socket.on("score_updated", (data) => {
            setScore(data.score);
        });

        return () => {
            socket.off("score_updated");
        };
    }, []);

    // Fetching hint usage from Flask on initial load
    useEffect(() => {
        axios.get("http://127.0.0.1:5000/api/get_hint_usage")
            .then(response => {
                // Update the hintUsage state with the data from Flask
                setHintUsage(response.data.hint_usage);
            })
            .catch(error => {
                console.error("Error fetching hint usage:", error);
            });
    }, []);

    // Function to update hintUsage in Flask whenever hintUsage changes
    useEffect(() => {
        if (hintUsage.length > 0) { 
            updateHintUsage();  
        }
    }, [hintUsage]); 

    // Function to update hintUsage in Flask
    const updateHintUsage = () => {
        axios.post("http://127.0.0.1:5000/api/update_hint_usage", {
            hint_usage: hintUsage
        })
        .then(response => {
            console.log("Hint usage updated:", response.data);
        })
        .catch(error => {
            console.error("Error updating hint usage:", error);
        });
    };

    const videoRef = useRef(null);
    const canvasRef = useRef(null);

    useEffect(() => {
        const hands = new Hands({
            locateFile: (file) => {
                return `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`;
            },
        });

        hands.setOptions({
            maxNumHands: 1,
            modelComplexity: 1,
            minDetectionConfidence: 0.5,
            minTrackingConfidence: 0.6,
        });

        hands.onResults((results) => {
            // Logging results to the console
            console.log("MediaPipe Results:", results);

            const canvas = canvasRef.current;
            const ctx = canvas.getContext("2d");

            // Clear canvas for each frame
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // Mirror canvas for webcam input
            ctx.save();
            ctx.translate(canvas.width, 0);
            ctx.scale(-1, 1);

            // Draw landmarks on canvas and send them to Flask
            if (results.multiHandLandmarks) {
                results.multiHandLandmarks.forEach((landmarks) => {
                    // Log each detected hand's landmarks to the console
                    console.log("Detected Hand Landmarks:", landmarks);

                    landmarks.forEach((lm) => {
                        const x = lm.x * canvas.width;
                        const y = lm.y * canvas.height;

                        // Draw landmarks on canvas
                        ctx.beginPath();
                        ctx.arc(x, y, 5, 0, 2 * Math.PI);
                        ctx.fillStyle = "red";
                        ctx.fill();
                    });

                    // Send landmarks to Flask in real-time via WebSocket
                    console.log("Sending landmarks:", landmarks);
                    socket.emit("send_landmarks", { landmarks: landmarks });
                });
            }

            ctx.restore();
        });

        // Start the camera stream and begin hand tracking
        const startCamera = async () => {
            const stream = await navigator.mediaDevices.getUserMedia({
                video: { width: 640, height: 480 },
            });
            videoRef.current.srcObject = stream;

            const camera = new Camera(videoRef.current, {
                onFrame: async () => {
                    await hands.send({ image: videoRef.current }); // Send the current video frame to MediaPipe
                },
                width: 640,  // Adjust the width and height based on your requirements
                height: 480, // Adjust the width and height based on your requirements
            });

            camera.start();
        };

        startCamera();

        return () => {
            // Cleanup code for unmounting if necessary
        };
    }, []);
    


    return (<>
        {/*Conditionally hide the welcome-screen based on initialPage */}
        <div className={`welcome-screen ${!initialPage ? 'hidden' : ''}`}>
                <BlurOverlay />
                <div>
                    <Greeting username={username} />
                    <LevelSelection handleLevelClick={handleLevelClick}/>
                    <HomeButton1 onClick={goToHome}/>
                    <StartButton onClick={handleStartClick} />
                </div>
            </div>

        <Header/>
        <div className='main-level-container'>
            <LevelNo level={currentLevel}/>
            <LevelLetters
                currentLetters={currentLetters} 
                completedLetters={completedLetters} 
                selectedLetter={selectedLetter} 
                handleLetterClick={handleLetterClick}
            />
            <Score score={score}/>
        </div>
        <div className='sign-related-container'>
            <div className='canvas-wrapper'>
                <video
                    ref={videoRef}
                    id="videoElement"
                    style={{ display: "block", width: "768px", height: "432px", 
                        position:"absolute"}}
                    width="768"
                    height="432"
                    autoPlay
                ></video>
                <Canvas/>
                <Timer/>
                <Notification/>
                <StartNote letter={selectedLetter} handleGameStartClick={handleGameStartClick}/>
                <StartCountdown countdownTime={countdownTime}/>
            </div>
            
            <Hint handleHintButtonClick={handleHintButtonClick}/>
            <LetterSwitch handleNextLetterButtonClick={handleNextLetterButtonClick} handlePreviousLetterButtonClick={handlePreviousLetterButtonClick}/>
        </div>
        <HomeButton onClick={goToHome}/>
    </>);
}

export default App
