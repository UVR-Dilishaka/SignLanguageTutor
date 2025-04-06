import React, { useEffect, useState } from "react";
import { useNavigate, Link, Outlet } from "react-router-dom";
import ProfileHeader from "../components/profileHeader";
import { fetchUserData } from "../util/fetchuser";
import Footer from "../components/Footer";
import "../profile.css";

const ProfilePage = () => {
  const [userData, setUserData] = useState({});
  const [students, setStudents] = useState([]);
  const [selectedStudentId, setSelectedStudentId] = useState(""); // NEW
  const navigate = useNavigate();

  useEffect(() => {
    const loadUserData = async () => {
      const data = await fetchUserData(navigate);
      if (data) {
        setUserData(data);
        if (data.isteacher) {
          fetchStudents();
        }
      }
    };

    const fetchStudents = async () => {
      try {
        const response = await fetch("http://localhost:5000/data/users");
        if (!response.ok) throw new Error("Failed to fetch students");
        const data = await response.json();
        setStudents(data.filter(student => !student.isteacher));
      } catch (error) {
        console.error("Error fetching students:", error);
      }
    };

    loadUserData();
  }, [navigate]);

  return (
    <div className="profile-container">
      <ProfileHeader username={userData.username} />
      <div className="profile-content">
        <div className="profile-left">
          <div className="userdetails">
            <p>{userData.isteacher ? "Teacher" : "Student"} : {userData.username}</p>
          </div>

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
