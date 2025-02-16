
import React from "react";
import Header from "./components/Header";
import HomeImg from "./components/HomeImg";
import SignupButton from "./components/SignupButton";
import Features from "./components/Features";

import "./App.css";
import Letters from "./components/Letters";
import Footer from "./components/Footer";

function App() {
  return (
    <div className="container">
      <Header />
      <HomeImg />
      <SignupButton text="🚀 Sign In" link="/signup" />
      <Features />
      <Letters />
      <Footer />

    </div>
  );
}

export default App;
