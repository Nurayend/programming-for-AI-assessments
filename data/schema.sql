-- database: :memory:
-- 1. Enable Foreign Key support (SQLite defaults to OFF)
PRAGMA foreign_keys = ON;

-- 2. Clean up old tables (for development/testing purposes)
DROP TABLE IF EXISTS Wellbeing_Surveys;
DROP TABLE IF EXISTS Submissions;
DROP TABLE IF EXISTS Attendance;
DROP TABLE IF EXISTS Assessments;
DROP TABLE IF EXISTS Students;

-- 3. Table Definitions

-- Table: Students
-- Stores basic identification for students.
CREATE TABLE Students (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL
);

-- Table: Assessments
-- Defines coursework or exams with deadlines.
CREATE TABLE Assessments (
    assessment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    deadline DATE NOT NULL,
    max_score INTEGER DEFAULT 100
);

-- Table: Attendance
-- Tracks weekly lecture attendance.
CREATE TABLE Attendance (
    attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    week_number INTEGER NOT NULL,
    lecture_date DATE NOT NULL,
    status TEXT CHECK(status IN ('Present', 'Absent', 'Late')),
    FOREIGN KEY (student_id) REFERENCES Students(student_id)
);

-- Table: Submissions
-- Links assessments to students and records grades.
-- This data supports the Course Director's need for performance analytics[cite: 24].
CREATE TABLE Submissions (
    submission_id INTEGER PRIMARY KEY AUTOINCREMENT,
    assessment_id INTEGER NOT NULL,
    student_id INTEGER NOT NULL,
    submission_date DATE,
    score REAL CHECK(score >= 0),
    FOREIGN KEY (assessment_id) REFERENCES Assessments(assessment_id),
    FOREIGN KEY (student_id) REFERENCES Students(student_id)
);

-- Table: Wellbeing_Surveys
-- Stores weekly survey responses.
-- Includes constraint: Stress levels must be 1-5.
CREATE TABLE Wellbeing_Surveys (
    survey_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    date DATE NOT NULL,
    stress_level INTEGER CHECK(stress_level BETWEEN 1 AND 5), 
    sleep_hours REAL CHECK(sleep_hours >= 0),
    FOREIGN KEY (student_id) REFERENCES Students(student_id)
);

-- 4. Insert Mock Data (for demonstration)

-- Insert Students
INSERT INTO Students (first_name, last_name, email) VALUES 
('San', 'Zhang', 'zhang.san@uni.ac.uk'),
('Si', 'Li', 'li.si@uni.ac.uk'),
('Wu', 'Wang', 'wang.wu@uni.ac.uk');

-- Insert Assessments
INSERT INTO Assessments (title, deadline, max_score) VALUES 
('Python Project', '2025-11-30', 100),
('Data Analysis Essay', '2025-12-15', 50);

-- Insert Attendance (Zhang San present, Li Si absent)
INSERT INTO Attendance (student_id, week_number, lecture_date, status) VALUES 
(1, 1, '2025-10-01', 'Present'),
(1, 2, '2025-10-08', 'Present'),
(2, 1, '2025-10-01', 'Absent');

-- Insert Wellbeing Surveys
-- Simulating a high-stress scenario for the Wellbeing Officer to detect[cite: 20].
INSERT INTO Wellbeing_Surveys (student_id, date, stress_level, sleep_hours) VALUES 
(1, '2025-10-01', 2, 7.5), -- Normal entry
(2, '2025-10-01', 5, 4.0), -- High stress
(2, '2025-10-08', 4, 5.0); -- High stress continued