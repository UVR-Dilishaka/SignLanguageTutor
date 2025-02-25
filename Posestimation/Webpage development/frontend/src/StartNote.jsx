function StartNote({letter, handleGameStartClick}){
    return(
        <>
            <div className="start-note">
                <p>Selected Letter : {letter}</p>
                <div className="start-button1" onClick={handleGameStartClick}>Start</div>
            </div>
        </>
    )
}

export default StartNote;