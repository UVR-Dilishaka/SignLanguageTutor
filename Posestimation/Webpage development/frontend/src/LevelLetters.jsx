import React, { useEffect } from "react";

function LevelLetters({ currentLetters, completedLetters, selectedLetter, handleLetterClick, gameStarted }) {
    useEffect(() => {
        const letterBoxes = document.querySelectorAll('.letter-box');
        
        letterBoxes.forEach((box) => {
            if (gameStarted) {
                box.style.pointerEvents = 'none';  // Disable clicks
            } else {
                box.style.pointerEvents = 'auto';  // Enable clicks
            }
        });
    }, [gameStarted]); // Re-run whenever gameStarted changes

    return (
        <div className="letter-box-container">
            {currentLetters.map((letter, index) => (
                <div 
                    key={index} 
                    className={`letter-box 
                        ${completedLetters.includes(letter) ? "completed" : ""} 
                        ${letter === selectedLetter ? "selected" : ""}`
                    }
                    onClick={() => handleLetterClick(letter)}
                >
                    <p>{letter}</p>
                </div>
            ))}
        </div>
    );
}

export default LevelLetters;



