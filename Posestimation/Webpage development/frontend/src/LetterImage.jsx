import { useEffect } from "react";

function LetterImage({selectedLetter, allLetters, letterWords,letterImages,letterWordImages}){
    useEffect(() => {
        const wordElement = document.querySelector(".letter-word");
        const imageElement = document.querySelector(".letter-image");

        const selectedLetterIndex = allLetters.indexOf(selectedLetter);

        wordElement.innerHTML = letterWords[selectedLetterIndex]
        //imageElement.innerHTML = letterImages[selectedLetterIndex]
    })

    return (<>
            <div className="letter-word-box">
                <p className="letter-word"></p>
                <div className="letter-image"></div>
            </div>
        </>
    )
}

export default LetterImage;