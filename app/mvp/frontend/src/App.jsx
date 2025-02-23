import 'bootstrap/dist/css/bootstrap.min.css';
import React from "react";
import Header from "./components/Header";
import Footer from "./components/Footer";
import Signup from "./pages/SignupPage";
import Home from "./pages/HomePage";
import Login from "./pages/LoginPage";
import Test from "./pages/TestPage";
import TeacherPortal from './pages/TeacherPortalPage';

import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import "./App.css";

function App() {

  return (
    <Router>
    <div className="container">
    
      <Header />
      <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="/login" element={<Login />} />
          <Route path="/testping" element={<Test />} />
          <Route path="/teacherportal" element={<TeacherPortal />} />
      </Routes>
      <Footer />

    </div>
    </Router>
  );
}

export default App;
