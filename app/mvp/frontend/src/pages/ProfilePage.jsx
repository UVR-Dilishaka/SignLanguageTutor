import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { jwtDecode } from "jwt-decode";

const ProfilePage = () => {
  const [userData, setUserData] = useState({});
  const navigate = useNavigate();

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        // Get token from local storage
        const accessToken = localStorage.getItem("access_token");
        if (!accessToken) {
          console.error("No access token found");
          navigate("/login"); // Redirect to login if no token
          return;
        }

        // Decode the token to extract username
        const decodedToken = jwtDecode(accessToken);
        const username = decodedToken.sub; // Adjust based on JWT structure

        if (!username) {
          console.error("Username not found in token");
          return;
        }

        // Fetch user data from backend
        const response = await fetch(`http://127.0.0.1:5000/data/user/${username}`, {
          method: "GET",
          headers: {
            "Authorization": `Bearer ${accessToken}`,
            "Content-Type": "application/json",
          },
        });

        const data = await response.json();
        if (response.ok) {
          setUserData(data);
        } else {
          console.error("Failed to fetch user data:", data.message);
        }
      } catch (error) {
        console.error("Error fetching user data:", error);
      }
    };

    fetchUserData();
  }, [navigate]);

  return (
    <div className="profile-page">
      <h1>Profile Page</h1>
      {userData.username ? (
        <div>
          <p><strong>Username:</strong> {userData.username}</p>
          <p><strong>Email:</strong> {userData.email}</p>
          <p><strong>Role:</strong> {userData.isteacher ? "Teacher" : "Student"}</p>
        </div>
      ) : (
        <p>Loading user data...</p>
      )}
    </div>
  );
};

export default ProfilePage;
