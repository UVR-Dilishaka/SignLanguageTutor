import React from "react";
import signImage from "../assets/homeimg.jpg"; // Place image in public/assets

const homeImg = () => {
  return (
    <div className="image-container">
      <img src={signImage} alt="Sign Language Display" />
    </div>
  );
};

export default homeImg;
