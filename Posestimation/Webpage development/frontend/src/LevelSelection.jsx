function LevelSelection({handleLevelClick}){
    return (
        <>
            <div className="level-container1">
                <p>Select Level</p>
                <div className="level-container2">
                    <div id="lvl1" className="level-select" onClick={() => handleLevelClick(1)}>🔒</div>
                    <div id="lvl2" className="level-select" onClick={() => handleLevelClick(2)}>🔒</div>
                    <div id="lvl3" className="level-select" onClick={() => handleLevelClick(3)}>🔒</div>
                    <div id="lvl4" className="level-select" onClick={() => handleLevelClick(4)}>🔒</div>
                </div>
            </div>
        </>
    )
}

export default LevelSelection;