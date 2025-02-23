import React, { useState, useEffect } from "react";
import "./TeacherPortal.css";

const TeacherPortal = () => {
    const [students, setStudents] = useState([]);
    const [selectedStudent, setSelectedStudent] = useState(null);
    const [masteryData, setMasteryData] = useState([]);

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

        fetchStudents();
    }, []);

    const handleStudentClick = async (studentId) => {
        setSelectedStudent(studentId);
        try {
            const response = await fetch(`http://localhost:5000/data/masteries/${studentId}`);
            if (!response.ok) throw new Error("Failed to fetch mastery levels");
            const data = await response.json();
            setMasteryData(data);
        } catch (error) {
            console.error("Error fetching mastery levels:", error);
        }
    };

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
                <h3>Mastery Levels</h3>
                {selectedStudent ? (
                    masteryData.length > 0 ? (
                        <ul>
                            {masteryData.map(sign => (
                                <li key={sign.sign_id}>
                                    Sign ID {sign.sign_id}: {sign.current_mastery_level}
                                </li>
                            ))}
                        </ul>
                    ) : <p>No data available</p>
                ) : <p>Select a student to view mastery levels</p>}
            </div>
        </div>
    );
};

export default TeacherPortal;
