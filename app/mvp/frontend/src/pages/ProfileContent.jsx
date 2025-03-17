import React, { useEffect, useState } from "react";
import { fetchUserData } from "../util/fetchuser";
import { useNavigate } from "react-router-dom";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";

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

  // Fetch all available signs
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

  // Fetch mastery data only after both userData and signs are available
  useEffect(() => {
    if (userData && signs.length > 0) {
      fetchMasteryData(userData.id);
    }
  }, [userData, signs]);

  // Fetch mastery levels of logged-in user
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

  // Filter mastery data based on selected language
  const filteredMasteryData = masteryData.filter(item => item.language === selectedLanguage);

  if (!userData) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <p><strong>Username:</strong> {userData.username}</p>
      <p><strong>Email:</strong> {userData.email}</p>
      <p><strong>Role:</strong> {userData.isteacher ? "Teacher" : "Student"}</p>

      {/* Student Performance Graph */}
      <div className="performance-section">
        <h3>Your Progress</h3>

        {/* Language Switching Buttons */}
        <div className="switch-buttons">
          <button 
            className={selectedLanguage === "Sinhala" ? "active" : ""}
            onClick={() => setSelectedLanguage("Sinhala")}
          >
            Sinhala Signs
          </button>
          <button 
            className={selectedLanguage === "Tamil" ? "active" : ""}
            onClick={() => setSelectedLanguage("Tamil")}
          >
            Tamil Signs
          </button>
        </div>

        {/* Bar Chart */}
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
    </div>
  );
};

export default ProfileContent;
