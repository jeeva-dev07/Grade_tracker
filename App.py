from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

# ---------------- DATABASE CONFIGURATION ----------------
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "YOUR_PASSWORD",  # Replace with your MySQL password
    "database": "grade_tracker"
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

# ---------------- GRADE CALCULATION LOGIC ----------------
def calculate_grade(percentage):
    if percentage >= 90:
        return {"grade": "A", "remark": "Excellent"}
    elif percentage >= 75:
        return {"grade": "B", "remark": "Good"}
    elif percentage >= 60:
        return {"grade": "C", "remark": "Average"}
    elif percentage >= 45:
        return {"grade": "D", "remark": "Below Average"}
    else:
        return {"grade": "F", "remark": "Fail"}

# ---------------- HOME ROUTE ----------------
@app.route("/")
def home():
    return jsonify({"message": "Student Grade Tracker API Running"})

# ---------------- ADD NEW STUDENT ----------------
@app.route("/students", methods=["POST"])
def add_student():
    data = request.json

    name = data.get("name")
    email = data.get("email")

    if not name or not email:
        return jsonify({"error": "Name and email required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        query = "INSERT INTO students (name, email) VALUES (%s, %s)"
        cursor.execute(query, (name, email))
        conn.commit()

        return jsonify({
            "message": "Student added successfully"
        }), 201

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 400

    finally:
        cursor.close()
        conn.close()

# ---------------- GET ALL STUDENTS ----------------
@app.route("/students", methods=["GET"])
def get_students():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM students")
        students = cursor.fetchall()

        return jsonify(students), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        cursor.close()
        conn.close()
@app.route("/students/<int:student_id>/marks", methods=["POST"])
def add_marks(student_id):

    data = request.json

    subject = data.get("subject")
    score = data.get("score")
    max_score = data.get("max_score", 100)

    if not subject or score is None:
        return jsonify({"error": "Subject and score required"}), 400

    try:
        score = float(score)
        max_score = float(max_score)

    except ValueError:
        return jsonify({
            "error": "Score and max_score must be numbers"
        }), 400

    if score < 0 or score > max_score:
        return jsonify({
            "error": "Invalid score values"
        }), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
  
        cursor.execute(
            "SELECT * FROM students WHERE id = %s",
            (student_id,)
        )

        student = cursor.fetchone()

        if not student:
            return jsonify({
                "error": "Student not found"
            }), 404

        query = """
        INSERT INTO marks (student_id, subject, score, max_score)
        VALUES (%s, %s, %s, %s)
        """

        cursor.execute(
            query,
            (student_id, subject, score, max_score)
        )

        conn.commit()

        return jsonify({
            "message": "Marks added successfully"
        }), 201

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        cursor.close()
        conn.close()

@app.route("/students/<int:student_id>/report", methods=["GET"])
def student_report(student_id):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(
            "SELECT * FROM students WHERE id = %s",
            (student_id,)
        )

        student = cursor.fetchone()

        if not student:
            return jsonify({
                "error": "Student not found"
            }), 404

        cursor.execute(
            """
            SELECT subject, score, max_score
            FROM marks
            WHERE student_id = %s
            """,
            (student_id,)
        )

        marks = cursor.fetchall()

        report = []

        total_score = 0
        total_max = 0

        for mark in marks:

            percentage = (
                float(mark["score"]) /
                float(mark["max_score"])
            ) * 100

            grade_data = calculate_grade(percentage)

            report.append({
                "subject": mark["subject"],
                "score": float(mark["score"]),
                "max_score": float(mark["max_score"]),
                "percentage": round(percentage, 2),
                "grade": grade_data["grade"],
                "remark": grade_data["remark"]
            })

            total_score += float(mark["score"])
            total_max += float(mark["max_score"])

        overall_percentage = (
            (total_score / total_max) * 100
            if total_max > 0 else 0
        )

        overall_grade = calculate_grade(overall_percentage)

        return jsonify({
            "student": student,
            "subjects": report,
            "overall_percentage": round(overall_percentage, 2),
            "overall_grade": overall_grade["grade"],
            "overall_remark": overall_grade["remark"]
        }), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        cursor.close()
        conn.close()

@app.route("/summary", methods=["GET"])
def summary():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # Total students
        cursor.execute("""
        SELECT COUNT(*) AS total_students
        FROM students
        """)

        total_students = cursor.fetchone()

        cursor.execute("""
        SELECT AVG((score / max_score) * 100)
        AS class_average
        FROM marks
        """)

        class_average = cursor.fetchone()

        # Top students
        top_students_query = """
        SELECT
            students.name,
            AVG((marks.score / marks.max_score) * 100)
            AS average_percentage
        FROM students
        JOIN marks
        ON students.id = marks.student_id
        GROUP BY students.id
        ORDER BY average_percentage DESC
        LIMIT 3
        """

        cursor.execute(top_students_query)

        top_students = cursor.fetchall()

        return jsonify({
            "total_students": total_students["total_students"],
            "class_average": round(
                class_average["class_average"], 2
            ) if class_average["class_average"] else 0,
            "top_students": top_students
        }), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        cursor.close()
        conn.close()

@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # Delete marks first
        cursor.execute(
            "DELETE FROM marks WHERE student_id = %s",
            (student_id,)
        )
      
        cursor.execute(
            "DELETE FROM students WHERE id = %s",
            (student_id,)
        )

        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({
                "error": "Student not found"
            }), 404

        return jsonify({
            "message": "Student deleted successfully"
        }), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
