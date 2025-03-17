// utils/fetchUserData.js
import { jwtDecode } from "jwt-decode";

export const fetchUserData = async (navigate) => {
  try {
    const accessToken = localStorage.getItem("access_token");
    if (!accessToken) {
      console.error("No access token found");
      navigate("/login");
      return null;
    }

    const decodedToken = jwtDecode(accessToken);
    const username = decodedToken.sub;

    if (!username) {
      console.error("Username not found in token");
      return null;
    }

    const response = await fetch(`http://127.0.0.1:5000/data/user/${username}`, {
      method: "GET",
      headers: {
        Authorization: `Bearer ${accessToken}`,
        "Content-Type": "application/json",
      },
    });

    const data = await response.json();
    if (response.ok) {
      return data;
    } else {
      console.error("Failed to fetch user data:", data.message);
      return null;
    }
  } catch (error) {
    console.error("Error fetching user data:", error);
    return null;
  }
};
