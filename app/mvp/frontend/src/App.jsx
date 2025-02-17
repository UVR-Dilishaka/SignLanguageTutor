import 'bootstrap/dist/css/bootstrap.min.css';
import React from "react";
import Header from "./components/Header";
import HomeImg from "./components/HomeImg";
import SignupButton from "./components/SignupButton";
import Features from "./components/Features";
import Letters from "./components/Letters";
import Footer from "./components/Footer";
import Signup from "./pages/Signuppage";

import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import "./App.css";

function App() {

  return (
    <Router>
    <div className="container">
    
      <Header />
      <Routes>
          <Route path="/" element={
            <>
              <HomeImg />
              <SignupButton text="🚀 Sign In" link="/signup" />
              <Features />
              <Letters />
            </>
          } />
          <Route path="/signup" element={<Signup />} />
      </Routes>
      <Footer />

    </div>
    </Router>
  );
}

export default App;
