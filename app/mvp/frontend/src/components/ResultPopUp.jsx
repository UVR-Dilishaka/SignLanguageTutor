const ResultPopup = ({ correctSigns, incorrectSigns, onClose }) => {
    return (
      <div className="popup-overlay">
        <div className="popup-content">
          <h2>Round Results</h2>
          <div>
            <h3>Correct Signs</h3>
            <ul>
              {correctSigns.map((sign, index) => (
                <li key={index} style={{ color: 'green' }}>
                  {sign}
                </li>
              ))}
            </ul>
          </div>
          <div>
            <h3>Incorrect Signs</h3>
            <ul>
              {incorrectSigns.map((sign, index) => (
                <li key={index} style={{ color: 'red' }}>
                  {sign}
                </li>
              ))}
            </ul>
          </div>
          <button onClick={onClose}>Next Round</button>
        </div>
      </div>
    );
  };

export default ResultPopup;  