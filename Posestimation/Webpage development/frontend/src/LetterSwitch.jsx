
function LetterSwitch({handleNextLetterButtonClick,handlePreviousLetterButtonClick}){
    return (
        <>  
        <div className="switch-button-container">
            <div className="next-letter-switch" onClick={handleNextLetterButtonClick}><p>Next Letter</p></div>
            <div className="previous-letter-switch" onClick={handlePreviousLetterButtonClick}><p>Previous Letter</p></div>
        </div>
        </>
    );
}

export default LetterSwitch;