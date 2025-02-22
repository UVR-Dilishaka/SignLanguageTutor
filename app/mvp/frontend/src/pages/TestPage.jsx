import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

function TestPage() {
  const [message, setMessage] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    const checkProtectedRoute = async () => {
      const token = localStorage.getItem("access_token");

      if (!token) {
        alert("No access token found, redirecting to login.");
        navigate("/login");
        return;
      }

      try {
        const response = await fetch("http://127.0.0.1:5000/data/ping-protected", {
          method: "GET",
          headers: {
            "Authorization": `Bearer ${token}`, // Send the access token in the Authorization header
          },
        });

        if (response.ok) {
          const data = await response.json();
          setMessage(data.txt); // Set the message from the protected route
        } else if (response.status === 401) {
          alert("Access denied or token expired. Redirecting to login.");
          navigate("/login");
        } else {
          alert("Failed to access protected route.");
        }
      } catch (error) {
        console.error("Error accessing protected route:", error);
        alert("Error occurred while fetching protected data.");
      }
    };

    checkProtectedRoute();
  }, [navigate]);

  return (
    <div className="container">
      <div className="form-container text-center">
        <h2>Protected Route Test</h2>
        <p>{message ? message : "Fetching data from the protected route..."}</p>
      </div>
    </div>
  );
}

export default TestPage;
