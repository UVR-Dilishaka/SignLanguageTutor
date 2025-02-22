import React, { useState } from "react";
import FormInput from "../components/FormInput";
import { Link, useNavigate } from "react-router-dom";
import "../App.css";

function LoginPage() {
  const [formData, setFormData] = useState({
    username: "",
    password: "",
  });

  const [errors, setErrors] = useState({});
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const validateForm = () => {
    let newErrors = {};
    if (!formData.username.trim()) newErrors.username = "Username is required";
    if (formData.password.length < 6) newErrors.password = "Password must be at least 6 characters long";

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (validateForm()) {
      try {
        const response = await fetch("http://127.0.0.1:5000/auth/login", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            username: formData.username,
            password: formData.password,
          }),
        });

        const data = await response.json();

        if (response.ok) {
          if (data.acess_token) {
            // Store access and refresh tokens in localStorage or sessionStorage
            localStorage.setItem("access_token", data.acess_token);
            localStorage.setItem("refresh_token", data.refresh_token);
            alert("Login successful");

            // Navigate to a different page after successful login (e.g., dashboard)
            navigate("/testping");
          } else {
            setErrors((prevErrors) => ({
              ...prevErrors,
              username: "Invalid username or password",
            }));
          }
        } else {
          alert("Login failed");
        }
      } catch (error) {
        console.error("Error during login:", error);
        alert("Login failed couldn't connect to server");
      }
    }
  };

  return (
    <div className="container">
      <div className="form-container text-center">
        <h2>Login</h2>
        <form className="auth-form" onSubmit={handleSubmit}>
          <FormInput
            label="Username"
            type="text"
            name="username"
            placeholder="Enter your username"
            value={formData.username}
            onChange={handleChange}
            error={errors.username}
          />

          <FormInput
            label="Password"
            type="password"
            name="password"
            placeholder="Enter your password"
            value={formData.password}
            onChange={handleChange}
            error={errors.password}
          />

          <button type="submit" className="btn btn-primary">Login</button>
        </form>
        <p>Don't have an account? <Link to="/signup"> Sign up </Link></p>
      </div>
    </div>
  );
}

export default LoginPage;
