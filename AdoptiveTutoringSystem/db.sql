-- Table for storing student information
CREATE TABLE student (
    student_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL,
    password_hash VARCHAR(255) NOT NULL
);

-- Table for storing teacher information
CREATE TABLE teacher (
    teacher_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL,
    password_hash VARCHAR(255) NOT NULL
);

-- Table for storing signs
CREATE TABLE signs (
    sign_id INT PRIMARY KEY AUTO_INCREMENT,
    language VARCHAR(50) NOT NULL,
    mono_code_characters VARCHAR(10) NOT NULL,
    predictive_label VARCHAR(50),
)

-- Table for storing activities (student interactions with signs)
CREATE TABLE activity (
    record_id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT NOT NULL,
    sign_id INT NOT NULL,
    result DECIMAL(5, 2) NOT NULL,  -- Result as success rate (e.g., 0.85 for 85%)
    timetaken DECIMAL(6, 2),  -- Time taken to perform the sign, in seconds
    hint_used BOOLEAN,  -- Whether a hint was used (true/false)
    hint_type VARCHAR(50),  -- Type of hint used (if applicable)
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES student(student_id),
    FOREIGN KEY (sign_id) REFERENCES signs(sign_id)
);

-- Table for tracking student performance history
CREATE TABLE performance_history (
    history_id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT NOT NULL,
    sign_id INT NOT NULL,
    mastery_level DECIMAL(5, 2),  -- Mastery level (e.g., 0.90 for 90%)
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES student(student_id),
    FOREIGN KEY (sign_id) REFERENCES signs(sign_id)
);

-- Table for tracking current mastery level of each sign for each student
CREATE TABLE student_sign_mastery (
    student_id INT NOT NULL,
    sign_id INT NOT NULL,
    current_mastery_level DECIMAL(5, 2),  -- Current mastery level (e.g., 0.90 for 90%)
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (student_id, sign_id),
    FOREIGN KEY (student_id) REFERENCES student(student_id),
    FOREIGN KEY (sign_id) REFERENCES signs(sign_id)
);
