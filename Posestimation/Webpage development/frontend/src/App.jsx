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
import { useEffect } from "react";


function App() {
    const [initialPage, setInitialPage] = useState(true);
    const [username, setUsername] = useState("Guest");
    const [currentLevel, setCurrentLevel] = useState(2);
    const [unlockedLevels, setUnlockedLevels] = useState([1,2,4])
    const [currentLetters, setCurrentLetters] = useState(['L1', 'L2', 'L3', 'L4','L5'])
    const [completedLetters, setCompletedLetters] = useState(['L1', 'L2']);
    const [selectedLetter, setSelectedLetter] = useState('L1')
    const [score, setScore] = useState(100)
    const [countdownTime, setCountdownTime] = useState(5);
    let allLetters = ['L1', 'L2', 'L3', 'L4', 'L5', 'L6', 'L7']
    let hintUsage = [true, false, true, false, false, false, false]


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
                <Canvas/>
                <Timer/>
                <Notification/>
                <StartNote letter={selectedLetter} handleGameStartClick={handleGameStartClick}/>
                <StartCountdown countdownTime={countdownTime}/>
            </div>
            
            <Hint/>
            <LetterSwitch/>
        </div>
        <HomeButton/>
    </>);
}

export default App
