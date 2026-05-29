
Student-Marks---Grade-Tracker-API
Repository navigation
Code
Issues
Pull requests
Student-Marks---Grade-Tracker-API
/README.md
venky1845
venky1845
50 minutes ago
444 lines (311 loc) · 5.07 KB

Preview

Code

Blame
Student Marks & Grade Tracker API
Project Overview
This project is a backend REST API built using Python Flask and MySQL.

The API manages:

Students
Subject marks
Grade calculation
Student reports
Class summary statistics
The project does not include a frontend. All endpoints are tested using Postman.

Technologies Used
Python
Flask
Flask-CORS
MySQL
MySQL Connector Python
Installation
1. Clone Repository
git clone https://github.com/your-username/student-grade-tracker-api.git
2. Install Dependencies
pip install flask flask-cors mysql-connector-python
3. Create MySQL Database
CREATE DATABASE grade_tracker;

USE grade_tracker;

CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE marks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    subject VARCHAR(100) NOT NULL,
    score DECIMAL(5,2) NOT NULL,
    max_score DECIMAL(5,2) NOT NULL DEFAULT 100,
    added_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (student_id)
    REFERENCES students(id)
    ON DELETE CASCADE
);
4. Update Database Credentials
Inside app.py:

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="grade_tracker"
)
5. Run the Application
python app.py
Server runs at:

http://localhost:5000
Grade Logic
Percentage	Grade
>= 90	A
>= 75	B
>= 60	C
>= 45	D
< 45	F
API Endpoints
Student Endpoints
GET /students
Get all students.

URL
http://localhost:5000/students
Response
[
  {
    "id": 1,
    "name": "Jeeva",
    "email": "jeeva@gmail.com"
  }
]
GET /students/
Get a student by ID.

Example
http://localhost:5000/students/1
Response
{
  "id": 1,
  "name": "Jeeva",
  "email": "jeeva@gmail.com"
}
POST /students
Add a new student.

Request Body
{
  "name": "Jeeva",
  "email": "jeeva@gmail.com"
}
Response
{
  "message": "Student added successfully"
}
PUT /students/
Update student details.

Request Body
{
  "name": "Jeeva",
  "email": "Jeeva@gmail.com"
}
Response
{
  "message": "Student updated successfully"
}
DELETE /students/
Delete a student and all marks.

Response
{
  "message": "Student deleted successfully"
}
Marks Endpoints
GET /students//marks
Get all marks for a student.

Example
http://localhost:5000/students/1/marks
Response
[
  {
    "subject": "Math",
    "score": 92,
    "max_score": 100,
    "percentage": 92,
    "grade": "A",
    "remarks": "Outstanding"
  }
]
POST /students//marks
Add marks for a student.

Request Body
{
  "subject": "Math",
  "score": 92,
  "max_score": 100
}
Response
{
  "message": "Marks added successfully",
  "percentage": 92,
  "grade": "A",
  "remarks": "Outstanding"
}
DELETE /marks/
Delete a mark entry.

Response
{
  "message": "Mark deleted successfully"
}
Report Endpoints
GET /students//report/summary/
Get complete student report.
