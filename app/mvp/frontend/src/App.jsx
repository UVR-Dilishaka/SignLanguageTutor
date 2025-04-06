import 'bootstrap/dist/css/bootstrap.min.css';
import React from "react";
import Signup from "./pages/SignupPage";
import Home from "./pages/HomePage";
import Login from "./pages/LoginPage";
import ProfilePage from "./pages/ProfilePage";
import ProfileContent from "./pages/ProfileContent";
import PlayPage from "./pages/PlayPage";


import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import "./App.css";

function App() {

  return (
    <Router>
    <div className="container">
    
      
      <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="/login" element={<Login />} />
          <Route path="/profile/*" element={<ProfilePage />}>
            <Route index element={<ProfileContent />} /> 
          </Route>
          <Route path="play" element={<PlayPage />} />
      </Routes>
      

    </div>
    </Router>
  );
}

export default App;
