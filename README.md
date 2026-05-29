# grade_tracker

## Project Overview

This project is a backend REST API built using Python Flask and MySQL.

The API manages:

* Students
* Subject marks
* Grade calculation
* Student reports
* Class summary statistics

The project does not include a frontend.
All endpoints are tested using Postman.

---

# Technologies Used

* Python
* Flask
* Flask-CORS
* MySQL
* MySQL Connector Python

---

# Installation

## 1. Clone Repository

```bash
git clone https://github.com/your-username/student-grade-tracker-api.git
```

---

## 2. Install Dependencies

```bash
pip install flask flask-cors mysql-connector-python
```

---

## 3. Create MySQL Database

```sql
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
```

---

## 4. Update Database Credentials

Inside `app.py`:

```python
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="grade_tracker"
)
```

---

## 5. Run the Application

```bash
python app.py
```

Server runs at:

```text
http://localhost:5000
```

---

# Grade Logic

| Percentage | Grade |
| ---------- | ----- |
| >= 90      | A     |
| >= 75      | B     |
| >= 60      | C     |
| >= 45      | D     |
| < 45       | F     |

---

# API Endpoints

# Student Endpoints

---

## GET /students

Get all students.

### URL

```text
http://localhost:5000/students
```

### Response

```json
[
  {
    "id": 1,
    "name": "Jeeva",
    "email": "jeeva@gmail.com"
  }
]
```

---

## GET /students/<id>

Get a student by ID.

### Example

```text
http://localhost:5000/students/1
```

### Response

```json
{
  "id": 1,
  "name": "Jeeva",
  "email": "jeeva@gmail.com"
}
```

---

## POST /students

Add a new student.

### Request Body

```json
{
  "name": "Jeeva",
  "email": "jeeva@gmail.com"
}
```

### Response

```json
{
  "message": "Student added successfully"
}
```

---

## PUT /students/<id>

Update student details.

### Request Body

```json
{
  "name": "Jeeva",
  "email": "jeeva@gmail.com"
}
```

### Response

```json
{
  "message": "Student updated successfully"
}
```

---

## DELETE /students/<id>

Delete a student and all marks.

### Response

```json
{
  "message": "Student deleted successfully"
}
```

---

# Marks Endpoints

---

## GET /students/<id>/marks

Get all marks for a student.

### Example

```text
http://localhost:5000/students/1/marks
```

### Response

```json
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
```

---

## POST /students/<id>/marks

Add marks for a student.

### Request Body

```json
{
  "subject": "Math",
  "score": 92,
  "max_score": 100
}
```

### Response

```json
{
  "message": "Marks added successfully",
  "percentage": 92,
  "grade": "A",
  "remarks": "Outstanding"
}
```

---

## DELETE /marks/<id>

Delete a mark entry.

### Response

```json
{
  "message": "Mark deleted successfully"
}
```

---

# Report Endpoints

---

## GET /students/<id>/report

Get complete student report.
