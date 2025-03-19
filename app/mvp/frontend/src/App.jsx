import 'bootstrap/dist/css/bootstrap.min.css';
import React from "react";
import Signup from "./pages/SignupPage";
import Home from "./pages/HomePage";
import Login from "./pages/LoginPage";
import Test from "./pages/TestPage";
import ProfilePage from "./pages/ProfilePage";
import TeacherPortal from './pages/TeacherPortalPage';
import ProfileContent from "./pages/ProfileContent";
import ReportPage from "./pages/ReportPage";
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
          <Route path="/testping" element={<Test />} />
          <Route path="/teacherportal" element={<TeacherPortal />} />
          <Route path="/profile/*" element={<ProfilePage />}>
            <Route index element={<ProfileContent />} /> {/* Set ProfileContent as the default route */}
            <Route path="report" element={<ReportPage />} />
            <Route path="play" element={<PlayPage />} />
          </Route>
          <Route path="/testpage" element={<Test />} />
      </Routes>
      

    </div>
    </Router>
  );
}

export default App;
