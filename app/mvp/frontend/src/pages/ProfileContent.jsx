import React, { useEffect, useState } from "react";
import { fetchUserData } from "../util/fetchuser";
import { useNavigate } from "react-router-dom";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, LineChart, Line } from "recharts";

const ProfileContent = () => {
  const [userData, setUserData] = useState(null);
  const [masteryData, setMasteryData] = useState([]);
  const [signs, setSigns] = useState([]);
  const [selectedLanguage, setSelectedLanguage] = useState("Sinhala"); // Default to Sinhala
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

  useEffect(() => {
    const fetchSigns = async () => {
      try {
        const response = await fetch("http://localhost:5000/data/signs");
        if (!response.ok) throw new Error("Failed to fetch signs");
        const data = await response.json();
        setSigns(data);
      } catch (error) {
        console.error("Error fetching signs:", error);
      }
    };
    fetchSigns();
  }, []);

  useEffect(() => {
    if (userData && signs.length > 0) {
      fetchMasteryData(userData.id);
    }
  }, [userData, signs]);

  const fetchMasteryData = async (userId) => {
    try {
      const response = await fetch(`http://localhost:5000/data/masteries/${userId}`);
      if (!response.ok) throw new Error("Failed to fetch mastery levels");
      const data = await response.json();
      setMasteryData(
        data.map(item => {
          const sign = signs.find(sign => sign.id === item.sign_id);
          return {
            ...item,
            mono_code_characters: sign ? sign.mono_code_characters : "Unknown",
            language: sign ? sign.language : "Unknown",
          };
        })
      );
    } catch (error) {
      console.error("Error fetching mastery levels:", error);
    }
  };

  const filteredMasteryData = masteryData.filter(item => item.language === selectedLanguage);

  const practiceData = [
    { date: "2025-03-18", signs_practiced: 5 },
    { date: "2025-03-19", signs_practiced: 7 },
    { date: "2025-03-20", signs_practiced: 3 },
    { date: "2025-03-21", signs_practiced: 8 },
    { date: "2025-03-22", signs_practiced: 6 },
  ];

  if (!userData) {
    return <div>Loading...</div>;
  }

  return (
    <div className="profile-report">
      <div className="userdetails">
        <p><strong>Username:</strong> {userData.username}</p>
        <p><strong>Email:</strong> {userData.email}</p>
        <p><strong>Role:</strong> {userData.isteacher ? "Teacher" : "Student"}</p>
      </div>

      <div className="switch-buttons">
        <button className={selectedLanguage === "Sinhala" ? "active" : ""} onClick={() => setSelectedLanguage("Sinhala")}>
          Sinhala Signs
        </button>
        <button className={selectedLanguage === "Tamil" ? "active" : ""} onClick={() => setSelectedLanguage("Tamil")}>
          Tamil Signs
        </button>
      </div>

      <div className="Graph-section">
        <div className="mastery-graph">
          {filteredMasteryData.length > 0 ? (
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={filteredMasteryData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="mono_code_characters" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="current_mastery_level" fill="#8884d8" />
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <p>No data available for {selectedLanguage} signs</p>
          )}
        </div>

        <div className="practice-graph">
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={practiceData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="signs_practiced" stroke="#82ca9d" />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};

export default ProfileContent;
