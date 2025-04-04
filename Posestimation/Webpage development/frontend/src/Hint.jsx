import { useEffect } from "react";

function Hint({handleHintButtonClick, selectedLetter, allLetters, hintImages}){
    useEffect(() => {
        const imageElement = document.querySelector(".hint-image");
        const selectedLetterIndex = allLetters.indexOf(selectedLetter);

        //imageElement.innerHTML = hintImages[selectedLetterIndex]
    })

    return (<>
        <div className="hint-container">
            <div className="hint-box">
                <p>Hint!</p>
                <div className="hint-image"></div>
            </div>
            <div className="hint-button" on onClick={handleHintButtonClick}>Use Hint </div>
        </div>
        </>
    )
}

export default Hint;