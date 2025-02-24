import React, { useState, useEffect } from "react";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";
import "../App.css";

const TeacherPortal = () => {
    const [students, setStudents] = useState([]);
    const [selectedStudent, setSelectedStudent] = useState(null);
    const [masteryData, setMasteryData] = useState([]);
    const [signs, setSigns] = useState([]);
    const [selectedLanguage, setSelectedLanguage] = useState("Sinhala"); // Default to Sinhala

    useEffect(() => {
        const fetchStudents = async () => {
            try {
                const response = await fetch("http://localhost:5000/data/users");
                if (!response.ok) throw new Error("Failed to fetch students");
                const data = await response.json();
                setStudents(data);
            } catch (error) {
                console.error("Error fetching students:", error);
            }
        };

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

        fetchStudents();
        fetchSigns();
    }, []);

    const handleStudentClick = async (studentId) => {
        setSelectedStudent(studentId);
        try {
            const response = await fetch(`http://localhost:5000/data/masteries/${studentId}`);
            if (!response.ok) throw new Error("Failed to fetch mastery levels");
            const masteryData = await response.json();

            const updatedMasteryData = masteryData.map(item => {
                const sign = signs.find(sign => sign.id === item.sign_id);
                return {
                    ...item,
                    mono_code_characters: sign ? sign.mono_code_characters : "Unknown",
                    language: sign ? sign.language : "Unknown"
                };
            });

            setMasteryData(updatedMasteryData);
        } catch (error) {
            console.error("Error fetching mastery levels:", error);
        }
    };

    // Filter mastery data based on selected language
    const filteredMasteryData = masteryData.filter(item => item.language === selectedLanguage);

    return (
        <div className="teacher-portal">
            <div className="sidebar">
                <h3>Students</h3>
                {students.map(student => (
                    <button 
                        key={student.id} 
                        className={selectedStudent === student.id ? "active" : ""}
                        onClick={() => handleStudentClick(student.id)}
                    >
                        {student.username}
                    </button>
                ))}
            </div>
            <div className="content">
                <h3>Student Performance</h3>
                {selectedStudent ? (
                    <>
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

                        {/* Chart */}
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
                    </>
                ) : (
                    <p>Select a student to view mastery levels</p>
                )}
            </div>
        </div>
    );
};

export default TeacherPortal;
