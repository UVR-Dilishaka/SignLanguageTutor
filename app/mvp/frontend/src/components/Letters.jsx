import React from "react";
import LetterCard from "./LetterCard";

const letters = [
  { text: "අ", color: "#FFAB91" },
  { text: "බ", color: "#80DEEA" },
  { text: "ස", color: "#A5D6A7" },
  { text: "ද", color: "#F48FB1" },
  { text: "ம", color: "#CE93D8" },
  { text: "க", color: "#FFCC80" },
  { text: "ந", color: "#9FA8DA" },
  { text: "ற", color: "#EF9A9A" },
];

const Letters = () => {
  return (
    <section>
      <h2>🔠 Learn the Letters</h2>
      <div className="letters">
        {letters.map((letter, index) => (
          <LetterCard key={index} text={letter.text} color={letter.color} />
        ))}
      </div>
    </section>
  );
};

export default Letters;
