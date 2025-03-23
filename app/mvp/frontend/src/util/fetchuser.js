import { jwtDecode } from "jwt-decode";

export const fetchUserData = async (navigate) => {
  try {
    let accessToken = localStorage.getItem("access_token");
    const refreshToken = localStorage.getItem("refresh_token");

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

    let response = await fetch(`http://127.0.0.1:5000/data/user/${username}`, {
      method: "GET",
      headers: {
        Authorization: `Bearer ${accessToken}`,
        "Content-Type": "application/json",
      },
    });

    if (response.status === 401 && refreshToken) {
      console.warn("Access token expired, attempting refresh...");
      
      // Attempt to refresh the token
      const refreshResponse = await fetch("http://127.0.0.1:5000/auth/refresh", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${refreshToken}`,
          "Content-Type": "application/json",
        },
      });

      if (refreshResponse.ok) {
        const refreshData = await refreshResponse.json();
        accessToken = refreshData.access_token;

        // Store the new access token
        localStorage.setItem("access_token", accessToken);

        // Retry the user data request with the new token
        response = await fetch(`http://127.0.0.1:5000/data/user/${username}`, {
          method: "GET",
          headers: {
            Authorization: `Bearer ${accessToken}`,
            "Content-Type": "application/json",
          },
        });
      } else {
        console.error("Failed to refresh token");
        navigate("/login");
        return null;
      }
    }

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
