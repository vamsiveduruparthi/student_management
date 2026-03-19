from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "student_management_secret"

# ---------------- DATABASE CONNECTION ----------------

def get_db():
    conn = sqlite3.connect("students.db")
    conn.row_factory = sqlite3.Row
    return conn


# ---------------- CREATE TABLE IF NOT EXISTS ----------------

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        course TEXT,
        email TEXT,
        phone TEXT,
        gender TEXT,
        date_of_birth TEXT,
        department TEXT,
        year_of_study TEXT,
        city TEXT,
        gpa REAL
    )
    """)

    conn.commit()
    conn.close()


init_db()


# ---------------- LOGIN ----------------

@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "admin123":
            session["admin"] = True
            return redirect("/admin")

        else:
            return render_template("login.html", error="HEY DUDE U R NOT MY ADMIN.")

    return render_template("login.html")


# ---------------- DASHBOARD ----------------

@app.route("/admin")
def admin():

    if "admin" not in session:
        return redirect("/")

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM students")
    total_students = cursor.fetchone()[0]

    conn.close()

    return render_template("admin.html", total_students=total_students)


# ---------------- VIEW STUDENTS ----------------

@app.route("/students")
def students():

    if "admin" not in session:
        return redirect("/")

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    conn.close()

    return render_template("view.html", students=students)


# ---------------- ADD STUDENT ----------------

@app.route("/add", methods=["GET", "POST"])
def add():

    if "admin" not in session:
        return redirect("/")

    if request.method == "POST":

        name = request.form["name"]
        age = request.form["age"]
        course = request.form["course"]
        email = request.form["email"]
        phone = request.form["phone"]
        gender = request.form["gender"]
        dob = request.form["date_of_birth"]
        department = request.form["department"]
        year = request.form["year_of_study"]
        city = request.form["city"]
        gpa = request.form["gpa"]

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO students
        (name, age, course, email, phone, gender, date_of_birth,
        department, year_of_study, city, gpa)

        VALUES (?,?,?,?,?,?,?,?,?,?,?)
        """,
        (name, age, course, email, phone, gender,
        dob, department, year, city, gpa)
        )

        conn.commit()
        conn.close()

        return redirect("/students")

    return render_template("add.html")


# ---------------- EDIT STUDENT ----------------

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):

    if "admin" not in session:
        return redirect("/")

    conn = get_db()
    cursor = conn.cursor()

    if request.method == "POST":

        name = request.form["name"]
        age = request.form["age"]
        course = request.form["course"]
        email = request.form["email"]
        phone = request.form["phone"]
        gender = request.form["gender"]
        dob = request.form["date_of_birth"]
        department = request.form["department"]
        year = request.form["year_of_study"]
        city = request.form["city"]
        gpa = request.form["gpa"]

        cursor.execute("""
        UPDATE students
        SET name=?, age=?, course=?, email=?, phone=?, gender=?, date_of_birth=?,
        department=?, year_of_study=?, city=?, gpa=?
        WHERE id=?
        """,
        (name, age, course, email, phone, gender, dob, department, year, city, gpa, id)
        )

        conn.commit()
        conn.close()

        return redirect("/students")

    cursor.execute("SELECT * FROM students WHERE id=?", (id,))
    student = cursor.fetchone()

    conn.close()

    return render_template("edit.html", student=student)


# ---------------- DELETE PAGE ----------------

@app.route("/delete/<int:id>")
def delete_page(id):

    if "admin" not in session:
        return redirect("/")

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students WHERE id=?", (id,))
    student = cursor.fetchone()

    conn.close()

    return render_template("delete.html", student=student)


# ---------------- DELETE CONFIRM ----------------

@app.route("/delete_confirm/<int:id>")
def delete_confirm(id):

    if "admin" not in session:
        return redirect("/")

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM students WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect("/students")


# ---------------- LOGOUT ----------------

@app.route("/logout")
def logout():

    session.clear()
    return redirect("/")


# ---------------- RUN APP ----------------

if __name__ == "__main__":
    app.run()