-- database: :memory:
-- 1. Enable Foreign Key support (SQLite defaults to OFF)
PRAGMA foreign_keys = ON;

-- 2. Clean up old tables (for development/testing purposes)
DROP TABLE IF EXISTS Wellbeing_Surveys;
DROP TABLE IF EXISTS Submissions;
DROP TABLE IF EXISTS Attendance;
DROP TABLE IF EXISTS Assessments;
DROP TABLE IF EXISTS Students;
DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Surveys;
DROP TABLE IF EXISTS Course_directors;
DROP TABLE IF EXISTS Roles;
DROP TABLE IF EXISTS Courses;

-- 3. Table Definitions

-- Table: Roles
-- Contains information about user roles (reference table)
CREATE TABLE Roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

-- Table: Users
-- Stores basic information for users
CREATE TABLE Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role_id INTEGER NOT NULL,
    FOREIGN KEY (role_id) REFERENCES Roles(id)
);

-- Table: Courses
-- Contains information about courses (reference table)
CREATE TABLE Courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

-- Table: Course_directors
-- Table linking the course and the course director (user)
CREATE TABLE Course_directors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(id),
    FOREIGN KEY (course_id) REFERENCES Courses(id),
    UNIQUE(user_id, course_id)
);

-- Table: Students
-- Stores basic identification for students
CREATE TABLE Students (
    id INTEGER PRIMARY KEY,
    course_id INTEGER NOT NULL,
    graduation_date DATE NOT NULL,
    status TEXT CHECK(status IN ('Active', 'Inactive')),
    FOREIGN KEY (course_id) REFERENCES Courses(id)
);

-- Table: Assessments
-- Defines coursework or exams with deadlines
CREATE TABLE Assessments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    course_id INTEGER NOT NULL,
    deadline DATE NOT NULL,
    max_score INTEGER DEFAULT 100,
    FOREIGN KEY (course_id) REFERENCES Courses(id)
);

-- Table: Attendance
-- Tracks weekly lecture attendance
CREATE TABLE Attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    lecture_date DATE NOT NULL,
    status TEXT CHECK(status IN ('Present', 'Absent', 'Late')),
    FOREIGN KEY (student_id) REFERENCES Students(id),
    FOREIGN KEY (course_id) REFERENCES Courses(id),
    UNIQUE(student_id, course_id, lecture_date)
);

-- Table: Submissions
-- Links assessments to students and records grades.
-- This data supports the Course Director's need for performance analytics
CREATE TABLE Submissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    assessment_id INTEGER NOT NULL,
    student_id INTEGER NOT NULL,
    submission_date DATE,
    score REAL CHECK(score >= 0),
    FOREIGN KEY (assessment_id) REFERENCES Assessments(id),
    FOREIGN KEY (student_id) REFERENCES Students(id),
    UNIQUE(student_id, assessment_id)
);

-- Table: Surveys
-- Contains information about surveys (reference table)
CREATE TABLE Surveys (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    passed_date DATE NOT NULL
);

-- Table: Wellbeing_Surveys
-- Stores weekly survey responses.
-- Includes constraint: Stress levels must be 1-5.
CREATE TABLE Wellbeing_Surveys (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    survey_id INTEGER NOT NULL,
    student_id INTEGER NOT NULL,
    stress_level INTEGER CHECK(stress_level BETWEEN 1 AND 5), 
    sleep_hours REAL CHECK(sleep_hours >= 0),
    FOREIGN KEY (student_id) REFERENCES Students(id),
    FOREIGN KEY (survey_id) REFERENCES Surveys(id),
    UNIQUE(student_id, survey_id)
);

-- 4. Insert Mock Data (for demonstration)

-- Insert Roles
INSERT INTO Roles (name) VALUES 
('Student Wellbeing Officer'),
('Student Wellbeing Officer Team'),
('Course Director');

-- Insert Users
INSERT INTO Users (username, password, role_id) VALUES 
('will_b', 'test123', 1),
('mike_w', 'test123', 2),
('lucas_s', 'test123', 3),
('dustin_h', 'test123', 3), 
('steve_h', 'test123', 3); 

-- Insert Courses
INSERT INTO Courses (name) VALUES 
('Statistics'),
('Programming'),
('FAIR');

INSERT INTO Course_directors (user_id, course_id) VALUES 
(3, 1),
(4, 2),
(5, 3);

-- Insert Students
INSERT INTO Students (id, course_id, graduation_date, status) VALUES 
(575001, 1, '2026-10-01', 'Active'),
(575002, 1, '2026-10-01', 'Active'),
(575003, 1, '2024-10-01', 'Active'),
(575004, 2, '2026-10-01', 'Active'),
(575005, 2, '2026-10-01', 'Active'),
(575006, 2, '2026-10-01', 'Inactive'),
(575007, 3, '2026-10-01', 'Active'),
(575008, 3, '2026-10-01', 'Active');

-- Insert Assessments
INSERT INTO Assessments (title, course_id, deadline, max_score) VALUES 
('Python Project', 2, '2025-11-30', 100),
('Data Analysis Essay', 3, '2025-12-15', 50),
('ANOVA Project', 1, '2025-12-15', 100);

-- Insert Submissions
INSERT INTO Submissions (assessment_id, student_id, submission_date, score) VALUES 
(1, 575001, '2025-11-15', 90),
(1, 575002, '2025-11-16', 80),
(1, 575003, '2025-11-15', 70),
(1, 575004, '2025-11-15', 60),
(1, 575005, '2025-11-30', 30), -- failed
(2, 575001, '2025-12-15', 80),
(2, 575002, '2025-12-15', 80),
(2, 575003, '2025-12-14', 0), -- failed
(3, 575001, '2025-12-15', 70),
(3, 575003, '2025-12-18', 40);

-- Insert Attendance
INSERT INTO Attendance (student_id, course_id, lecture_date, status) VALUES 
(575001, 1, '2025-10-01', 'Present'),
(575002, 1, '2025-10-08', 'Present'),
(575003, 1, '2025-10-08', 'Present'),
(575004, 1, '2025-10-08', 'Present'),
(575005, 1, '2025-10-08', 'Present'),
(575007, 1, '2025-10-08', 'Absent'),
(575001, 2, '2025-10-01', 'Absent'),
(575002, 2, '2025-10-01', 'Present'),
(575007, 2, '2025-10-08', 'Absent'),
(575007, 3, '2025-10-08', 'Absent'),
(575006, 3, '2025-10-01', 'Present');

-- Insert Surveys
INSERT INTO Surveys (passed_date) VALUES 
('2025-12-01'),
('2025-12-07'),
('2025-12-14');

-- Insert Wellbeing Surveys
-- Simulating a high-stress scenario for the Wellbeing Officer to detect
INSERT INTO Wellbeing_Surveys (student_id, survey_id, stress_level, sleep_hours) VALUES 
(575001, 1, 2, 7.5), -- Normal entry
(575002, 2, 5, 4.0), -- High stress
(575002, 3, 4, 5.0), -- High stress continued
(575003, 1, 4, 6.0),
(575003, 2, 4, 4.0),
(575001, 2, 1, 8.0);