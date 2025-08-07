from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# ------------------------
# Database Setup
# ------------------------
def init_db():
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS students (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        roll TEXT NOT NULL UNIQUE,
                        department TEXT NOT NULL,
                        email TEXT NOT NULL
                    )''')
    conn.commit()
    conn.close()

init_db()

# ------------------------
# Routes
# ------------------------

# Home - View all students
@app.route('/')
def index():
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    conn.close()
    return render_template('index.html', students=students)

# Add student
@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        roll = request.form['roll']
        department = request.form['department']
        email = request.form['email']
        
        conn = sqlite3.connect('students.db')
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO students (name, roll, department, email) VALUES (?, ?, ?, ?)",
                        (name, roll, department, email))
            conn.commit()
        except sqlite3.IntegrityError:
            return "Roll number or email already exists."
        finally:
            conn.close()
        return redirect(url_for('index'))
    
    return render_template('add.html')

# Delete student
@app.route('/delete/<int:student_id>')
def delete_student(student_id):
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)



#------------to run ----------------
# python app.py
