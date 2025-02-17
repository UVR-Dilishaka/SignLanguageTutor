import React from "react";
import signImage from "../assets/homeimg.jpg"; 

const HomeImg = () => {
  return (
    <div className="image-container">
      <img src={signImage} alt="Sign Language Display" />
    </div>
  );
};

export default HomeImg;
