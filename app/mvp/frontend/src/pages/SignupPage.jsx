import React, { useState } from "react";
import FormInput from "../components/FormInput";
import CheckboxInput from "../components/CheckboxInput";
import { Link } from "react-router-dom";
import "../App.css";
import Header from "../components/Header";

function Signuppage() {
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
    confirmPassword: "",
    isTeacher: false,
  });

  const [errors, setErrors] = useState({});

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === "checkbox" ? checked : value,
    });
  };

  const validateForm = () => {
    let newErrors = {};
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (!formData.username.trim()) newErrors.username = "Username is required";
    if (!emailRegex.test(formData.email)) newErrors.email = "Invalid email format";
    if (formData.password.length < 6) newErrors.password = "Password must be at least 6 characters long";
    if (formData.password !== formData.confirmPassword) newErrors.confirmPassword = "Passwords do not match";

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (validateForm()) {
      try {
        const response = await fetch("http://127.0.0.1:5000/auth/signup", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            username: formData.username,
            email: formData.email,
            password: formData.password,
            isteacher: formData.isTeacher,
          }),
        });

        const data = await response.json();

        if (response.ok) {
          if(data == 400){
            setErrors((prevErrors) => ({
              ...prevErrors,
              username: "Username already exists",
            }));

          }
          else if(data == 201){
            alert("Signup successful");
            setFormData({
              username: "",
              email: "",
              password: "",
              confirmPassword: "",
              isTeacher: false,
            });
          }
        } else
        {
          alert("Signup failed");
        }
      } catch (error) {
        console.error("Error during signup:", error);
        alert("Signup failed couldn't connect to server");
      }
    }
  };

  return (
    <>
    <Header />
    <div className="container">
      <div className="form-container text-center">
        <h2 className="auth-form-title" >Sign Up</h2>
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
            label="Email"
            type="email"
            name="email"
            placeholder="Enter your email"
            value={formData.email}
            onChange={handleChange}
            error={errors.email}
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

          <FormInput
            label="Confirm Password"
            type="password"
            name="confirmPassword"
            placeholder="Confirm your password"
            value={formData.confirmPassword}
            onChange={handleChange}
            error={errors.confirmPassword}
          />

          <CheckboxInput
            name="isTeacher"
            checked={formData.isTeacher}
            onChange={handleChange}
            label="I am a teacher"
          />

          <button type="submit" className="btn btn-primary">Sign Up</button>
        </form>
        <p>Already have an account? <Link to="/login"> Login </Link></p>
      </div>
    </div>
    </>
  );
}

export default Signuppage;
