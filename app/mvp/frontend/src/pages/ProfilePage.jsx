import React, { useEffect, useState } from "react";
import { useNavigate, Link, Outlet } from "react-router-dom";
import ProfileHeader from "../components/profileHeader";
import { fetchUserData } from "../util/fetchuser";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";
import Footer from "../components/Footer";
import "../profile.css";

const ProfilePage = () => {
  const [userData, setUserData] = useState({});
  const [masteryData, setMasteryData] = useState([]);
  const [signs, setSigns] = useState([]);
  const [selectedLanguage, setSelectedLanguage] = useState("Sinhala"); 
  const navigate = useNavigate();

  useEffect(() => {
    const loadUserData = async () => {
      const data = await fetchUserData(navigate);
      if (data) {
        setUserData(data);
        
      }
    };

    loadUserData();
    
  }, [navigate]);

  

  return (
    <div className="profile-container">
      <ProfileHeader username={userData.username} />
      <div className="profile-content">
        <div className="profile-left">
          <nav className="profile-menu">
            <Link to="/profile" className="menu-item">Profile</Link>
            <Link to="/play" className="menu-item">Play</Link>
          </nav>
        </div>

        <div className="profile-right">
          <div className="profile-switchcard">
            <Outlet />
          </div>
        </div>

      </div>
      <Footer />
    </div>
  );
};

export default ProfilePage;
