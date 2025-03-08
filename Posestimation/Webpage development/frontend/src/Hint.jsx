
function Hint({handleHintButtonClick}){
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