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
    const [gameRunning, setgameRunning] = useState(false);
    
    
    // State variables for running game
    const notificationRef = useRef(null);
    const [withinDistance, setwithinDistance] = useState(true); // Check if the hand is within specified distance
    const [notDetectingHands, setNotDetectingHands] = useState(false); // Check if landmark arrays are empty
    const [matches, setMatches] = useState(false); // If the backend detects the sign
    const [timeLeft, setTimeLeft] = useState(10);
    const [successNotficationNeeded, setSuccessNotificationNeeded] = useState(false)
    const [timesupNotificationNeeded, setTimesupNotificationNeeded] = useState(false)
    

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
        setgameRunning(false);
        setMatches(false);
        setSuccessNotificationNeeded(false);
        setTimesupNotificationNeeded(false);
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
        const countdownTimer = setInterval(() => {
            setCountdownTime(prevTime => {
                if (prevTime <= 1) {
                    clearInterval(countdownTimer);
                    if (countdown) countdown.style.display = "none";
    
                    // Start the game timer AFTER the countdown is done
                    startGameTimer();
                    
                    return 0;
                }
                return prevTime - 1;
            });
        }, 1000);
    };
    
    const startGameTimer = () => {
        let timeLeft = 20000; // 10 seconds
    
        const gameTimer = setInterval(() => {
            // 1. While timer is running (Update variables here)
            setgameRunning(true);
            console.log(`Time left: ${timeLeft / 1000}s`);
            let timeRemaining = (Math.floor(timeLeft/1000))
            document.querySelector('.timer').innerHTML = `You have : ${timeRemaining}`
    
            if (matches) {
                // 3. If matches become true (Stop timer and log time)
                setgameRunning(false);
                setTimeLeft(timeLeft);
                console.log(`Match detected at time: ${timeLeft / 1000}s`);
                document.querySelector('.canvas').style.display = 'none'
                document.querySelector('#videoElement').style.display = 'none'
                setSuccessNotificationNeeded(true)
                clearInterval(gameTimer);
                return;
            }
    
            timeLeft -= 50; // Decrease time by 50ms per frame
    
            if (timeLeft <= 0) {
                // 2. If time is out (Handle timeout scenario)
                setgameRunning(false);
                clearInterval(gameTimer);
                console.log("Timer finished. No match detected.");
                document.querySelector('.canvas').style.display = 'none'
                document.querySelector('#videoElement').style.display = 'none'
                setTimesupNotificationNeeded(true)
                return;
            }
        }, 50); // Runs every 50ms
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
        initialMoment()
    }

    //Handling previous letter button click
    const handlePreviousLetterButtonClick = () => {
        const prevLetter = currentLetters[currentLetters.indexOf(selectedLetter) - 1]
        setSelectedLetter(prevLetter)
        initialMoment();
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

    // Fucntion to update flask variable whenever selectedLetter changes
    useEffect(() => {
        if (selectedLetter) {
            socket.emit("update_selected_letter", { letter: selectedLetter });
        }
    }, [selectedLetter]);

    


    // useEffect function for detecting landmarks and sending them via websockets
    useEffect(() => {
        if (gameRunning === true && matches === false) {
            const videoElement = document.getElementById("videoElement");
            const canvasElement = document.querySelector(".canvas");
            const ctx = canvasElement.getContext("2d");
            const timer = document.querySelector(".timer")

            videoElement.style.display = 'block'
            canvasElement.style.display = 'block'
            timer.style.display = 'block'
    
            const hands = new Hands({
                locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`,
            });
    
            hands.setOptions({
                maxNumHands: 1,
                modelComplexity: 1,
                minDetectionConfidence: 0.5,
                minTrackingConfidence: 0.6,
            });
    
            hands.onResults((results) => {
                ctx.clearRect(0, 0, canvasElement.width, canvasElement.height);
    
                ctx.save();
                ctx.translate(canvasElement.width, 0);
                ctx.scale(-1, 1);
    
                if (results.multiHandLandmarks && results.multiHandLandmarks.length > 0) {
                    setNotDetectingHands(false)
                    results.multiHandLandmarks.forEach((landmarks) => {
                        landmarks.forEach((lm) => {
                            const x = lm.x * canvasElement.width;
                            const y = lm.y * canvasElement.height;
    
                            ctx.beginPath();
                            ctx.arc(x, y, 8, 0, 2 * Math.PI);
                            ctx.fillStyle = "GreenYellow";
                            ctx.fill();
                        });
                    });
    
                    const handData = results.multiHandLandmarks.map(hand => 
                        hand.map(lm => [lm.x, lm.y, lm.z])
                    );
    
                    socket.emit("hand_landmarks", { hands: handData });
    
    
                    // Calculate reference line lengths
                    const wrist = handData[0][0]; // Corrected indexing
                    const middle_mcp = handData[0][9];
    
                    const refLine1Length = Math.sqrt(
                        (middle_mcp[0] - wrist[0]) ** 2 +
                        (middle_mcp[1] - wrist[1]) ** 2 +
                        (middle_mcp[2] - wrist[2]) ** 2
                    );
    
                    const index_mcp = handData[0][5];
                    const pinky_mcp = handData[0][17];
    
                    const refLine2Length = Math.sqrt(
                        (index_mcp[0] - pinky_mcp[0]) ** 2 +
                        (index_mcp[1] - pinky_mcp[1]) ** 2 +
                        (index_mcp[2] - pinky_mcp[2]) ** 2
                    );
    
                    if (refLine1Length < 0.25 && refLine2Length < 0.10){
                        setwithinDistance(false)
                    } else {
                        setwithinDistance(true)
                    }
                } else if (results.multiHandLandmarks && results.multiHandLandmarks.length === 0){
                    setNotDetectingHands(true);
                }
    
                ctx.restore();
            });
    
            async function startCamera() {
                const stream = await navigator.mediaDevices.getUserMedia({
                    video: { width: 1280, height: 720 },
                });
                videoElement.srcObject = stream;
    
                const camera = new Camera(videoElement, {
                    onFrame: async () => {
                        await hands.send({ image: videoElement });
                    },
                    width: 1280,
                    height: 720,
                });
    
                camera.start();
            }
    
            startCamera();
    
            return () => {
                hands.close();
                videoElement?.srcObject?.getTracks().forEach(track => track.stop());
            };
        }
    }, [gameRunning, matches]);
    

    

    // useEffect function for handling notification displaying 
    useEffect(() => {
        const notificationBox = notificationRef.current
        const canvas = document.querySelector('.canvas')
        const videoElement = document.querySelector('#videoElement')

        notificationBox.style.display = 'none'
        canvas.style.filter = 'none';
        videoElement.style.filter = 'none';

        // If the hands are not detecting
        if (gameRunning === true && notDetectingHands === true) {
            notificationBox.style.display = "block"
            notificationBox.innerHTML = "⚠️ Can't detect any hands in the frame"
            canvas.style.filter = "blur(5px)";
            videoElement.style.filter = "blur(5px)";
        }
        
        // If the hands are not in the distance
        else if (gameRunning ==true && withinDistance === false){
            notificationBox.style.display = "block"
            notificationBox.innerHTML = "⚠️ Please move hands closer to the camera"
            canvas.style.filter = "blur(5px)";
            videoElement.style.filter = "blur(5px)";
        }

        // If the completed
        else if (successNotficationNeeded === true){
            let countdown = 5;
            notificationBox.style.display = "block";
            notificationBox.style.backgroundColor = "hsl(148, 100%, 84%)";
            canvas.style.filter = "blur(5px)";
            videoElement.style.filter = "blur(5px)";

            const timer = setInterval(() => {
                notificationBox.innerHTML = `✅ Well done! The sign matches <br> This message will close in ${countdown}`;

                if (countdown-- === 0) {
                    clearInterval(timer);
                    notificationBox.style.display = "none";
                    canvas.style.filter = "none";
                    videoElement.style.filter = "none";
                    initialMoment()
                }
            }, 1000);
        }

        // If couldn't complete
        else if (timesupNotificationNeeded === true){
            let countdown = 5;
            notificationBox.style.display = "block";
            notificationBox.style.backgroundColor = "hsl(0, 100%, 88%)";
            canvas.style.filter = "blur(5px)";
            videoElement.style.filter = "blur(5px)";

            const timer = setInterval(() => {
                notificationBox.innerHTML = `⌛ Time's up, better luck next time <br> This message will close in ${countdown}`;

                if (countdown-- === 0) {
                    clearInterval(timer);
                    notificationBox.style.display = "none";
                    canvas.style.filter = "none";
                    videoElement.style.filter = "none";
                    initialMoment()
                }
            }, 1000);
        }

    }, [gameRunning, notDetectingHands, withinDistance, successNotficationNeeded, timesupNotificationNeeded]);

    
    


    
    
    
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
                    id="videoElement"
                    style={{ display: "block", width: "768px", height: "432px", 
                        position:"absolute", transform: "scaleX(-1)", zIndex: "2"}}
                    width="768"
                    height="432"
                    autoPlay
                ></video>
                <canvas className='canvas' width="1280" height="720"></canvas>
                <div className="timer" >You have:</div>
                <Notification ref={notificationRef}/>
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
