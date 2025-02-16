import React from "react";

const LetterCard = ({ text, color }) => {
  return (
    <div className="letter" style={{ backgroundColor: color }}>
      {text}
    </div>
  );
};

export default LetterCard;
