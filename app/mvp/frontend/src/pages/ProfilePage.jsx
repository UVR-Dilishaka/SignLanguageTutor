import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { 
  BarChart, Bar, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer 
} from "recharts";

function ProfilePage() {
  const navigate = useNavigate();

  const user = {
    name: "John Doe",
    username: "johndoe123",
    email: "johndoe@example.com",
    role: "Student", 
    profilePic: "https://via.placeholder.com/150", 
  };

  // Tamil sign letter accuracy (12 letters)
  const tamilData = [
    { letter: "அ", accuracy: 85 },
    { letter: "ஆ", accuracy: 90 },
    { letter: "இ", accuracy: 78 },
    { letter: "ஈ", accuracy: 88 },
    { letter: "உ", accuracy: 92 },
    { letter: "ஊ", accuracy: 80 },
    { letter: "எ", accuracy: 86 },
    { letter: "ஏ", accuracy: 89 },
    { letter: "ஐ", accuracy: 94 },
    { letter: "ஒ", accuracy: 82 },
    { letter: "ஓ", accuracy: 87 },
    { letter: "ஔ", accuracy: 91 },
  ];

  // Sinhala sign letter accuracy (18 letters)
  const sinhalaData = [
    { letter: "අ", accuracy: 83 },
    { letter: "ආ", accuracy: 89 },
    { letter: "ඇ", accuracy: 75 },
    { letter: "ඈ", accuracy: 85 },
    { letter: "ඉ", accuracy: 91 },
    { letter: "ඊ", accuracy: 79 },
    { letter: "උ", accuracy: 84 },
    { letter: "ඌ", accuracy: 88 },
    { letter: "ඍ", accuracy: 90 },
    { letter: "ඎ", accuracy: 76 },
    { letter: "එ", accuracy: 87 },
    { letter: "ඒ", accuracy: 92 },
    { letter: "ඓ", accuracy: 81 },
    { letter: "ඔ", accuracy: 86 },
    { letter: "ඕ", accuracy: 93 },
    { letter: "ඖ", accuracy: 80 },
    { letter: "඘", accuracy: 78 },
    { letter: "ඝ", accuracy: 88 },
  ];

  const [selectedLanguage, setSelectedLanguage] = useState("Tamil");

  // Update chart based on language selection
  const letterData = selectedLanguage === "Tamil" ? tamilData : sinhalaData;

  // Redirect to Play Page with selected language
  const goToPlayPage = () => {
    navigate("/play", { state: { selectedLanguage } });
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100 p-6 space-y-6">
      
      {/* User Details Container */}
      <div className="details-container bg-indigo-100 border-2 border-indigo-500 shadow-xl rounded-2xl p-6 max-w-md w-full">
        <div className="flex flex-col items-center">
          <img
            src={user.profilePic}
            alt="Profile"
            className="w-32 h-32 rounded-full border-4 border-indigo-500"
          />
          <div className="text-center mt-4">
            <h2 className="text-2xl font-semibold text-gray-800">{user.name}</h2>
            <p className="text-gray-600">@{user.username}</p>
            <p className="text-gray-600">{user.email}</p>
            <span className="inline-block bg-indigo-500 text-white px-4 py-1 rounded-full mt-2">
              {user.role}
            </span>
          </div>
        </div>
        <button className="mt-6 w-full bg-red-500 text-white py-2 rounded-lg shadow-md hover:bg-red-600">
          Logout
        </button>
      </div>

      {/* Performance Container */}
      <div className="performance-container bg-gray-200 border-2 border-gray-500 shadow-xl rounded-2xl p-6 max-w-2xl w-full">
        <h3 className="text-xl font-semibold text-center text-gray-800 mb-4">
          Performance on {selectedLanguage} Sign Letters
        </h3>

        {/* Bar Chart */}
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={letterData}>
            <XAxis dataKey="letter" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="accuracy" fill="#4F46E5" />
          </BarChart>
        </ResponsiveContainer>

        {/* Language Selection & Play Button */}
        <div className="flex justify-between mt-6">
          <select
            value={selectedLanguage}
            onChange={(e) => setSelectedLanguage(e.target.value)}
            className="custom-select"
          >
            <option value="Tamil">Tamil</option>
            <option value="Sinhala">Sinhala</option>
          </select>

          <button className="custom-button" onClick={goToPlayPage}>
          
            Play
          </button>
        </div>
      </div>
    </div>
  );
}

export default ProfilePage;
