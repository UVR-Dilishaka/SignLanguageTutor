import React, { useEffect } from "react";

function LetterSwitch({ handleNextLetterButtonClick, handlePreviousLetterButtonClick, gameStarted }) {
    useEffect(() => {
        const buttons = document.querySelectorAll('.next-letter-switch, .previous-letter-switch');

        buttons.forEach((button) => {
            if (gameStarted) {
                button.style.pointerEvents = 'none';  // Disable clicks
            } else {
                button.style.pointerEvents = 'auto';  // Enable clicks
            }
        });
    }, [gameStarted]); // Re-run whenever gameStarted changes

    return (
        <>  
            <div className="switch-button-container">
                <div className="next-letter-switch" onClick={handleNextLetterButtonClick}>
                    <p>Next Letter</p>
                </div>
                <div className="previous-letter-switch" onClick={handlePreviousLetterButtonClick}>
                    <p>Previous Letter</p>
                </div>
            </div>
        </>
    );
}

export default LetterSwitch;
