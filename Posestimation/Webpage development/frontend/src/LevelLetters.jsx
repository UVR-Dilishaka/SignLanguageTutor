import React from "react";

function LevelLetters({ currentLetters, completedLetters, selectedLetter, handleLetterClick }) {
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
