import streamlit as st
import sqlite3

# ---------------------------
# Database Functions
# ---------------------------
def create_table():
    conn = sqlite3.connect("fashion_students.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                age INTEGER,
                gender TEXT,
                email TEXT,
                phone TEXT,
                course TEXT
            )""")
    conn.commit()
    conn.close()

def add_student(name, age, gender, email, phone, course):
    conn = sqlite3.connect("fashion_students.db")
    c = conn.cursor()
    c.execute("INSERT INTO students (name, age, gender, email, phone, course) VALUES (?, ?, ?, ?, ?, ?)",
              (name, age, gender, email, phone, course))
    conn.commit()
    conn.close()

def get_students():
    conn = sqlite3.connect("fashion_students.db")
    c = conn.cursor()
    c.execute("SELECT * FROM students")
    data = c.fetchall()
    conn.close()
    return data

def update_student(student_id, name, age, gender, email, phone, course):
    conn = sqlite3.connect("fashion_students.db")
    c = conn.cursor()
    c.execute("""UPDATE students SET name = ?, age = ?, gender = ?, email = ?, phone = ?, course = ?
                 WHERE id = ?""", (name, age, gender, email, phone, course, student_id))
    conn.commit()
    conn.close()

def delete_student(student_id):
    conn = sqlite3.connect("fashion_students.db")
    c = conn.cursor()
    c.execute("DELETE FROM students WHERE id = ?", (student_id,))
    conn.commit()
    conn.close()

# ---------------------------
# UI
# ---------------------------
st.set_page_config(page_title="Fashion Course Registration", page_icon="🧵")
st.title("🧵 Fashion Course Student Registration")

menu = ["Add Student", "View Students", "Update Student", "Delete Student"]
choice = st.sidebar.selectbox("Navigation", menu)

create_table()

# ---------------------------
# Add Student
# ---------------------------
if choice == "Add Student":
    st.subheader("📋 Register a New Student")
    name = st.text_input("Full Name")
    age = st.number_input("Age", min_value=15, max_value=60, step=1)
    gender = st.selectbox("Gender", ["Female", "Male", "Other"])
    email = st.text_input("Email")
    phone = st.text_input("Phone Number")
    course = st.selectbox("Fashion Course", ["Fashion Designing", "Textile Designing", "Fashion Merchandising", "Makeup & Styling", "Fashion Communication"])

    if st.button("Register"):
        if name and email and phone:
            add_student(name, age, gender, email, phone, course)
            st.success(f"✅ {name} has been registered!")
        else:
            st.error("❗ Please fill in all required fields.")

# ---------------------------
# View Students
# ---------------------------
elif choice == "View Students":
    st.subheader("📑 Registered Students")
    students = get_students()
    if students:
        st.dataframe(students, use_container_width=True)
    else:
        st.info("No students found.")

# ---------------------------
# Update Student
# ---------------------------
elif choice == "Update Student":
    st.subheader("✏️ Update Student Details")
    students = get_students()
    if students:
        student_dict = {f"{s[1]} (ID: {s[0]})": s for s in students}
        selected = st.selectbox("Select Student to Update", list(student_dict.keys()))
        student = student_dict[selected]
        student_id = student[0]

        name = st.text_input("Full Name", student[1])
        age = st.number_input("Age", min_value=15, max_value=60, value=student[2])
        gender = st.selectbox("Gender", ["Female", "Male", "Other"], index=["Female", "Male", "Other"].index(student[3]))
        email = st.text_input("Email", student[4])
        phone = st.text_input("Phone Number", student[5])
        course = st.selectbox("Fashion Course", ["Fashion Designing", "Textile Designing", "Fashion Merchandising", "Makeup & Styling", "Fashion Communication"],
                              index=["Fashion Designing", "Textile Designing", "Fashion Merchandising", "Makeup & Styling", "Fashion Communication"].index(student[6]))

        if st.button("Update"):
            update_student(student_id, name, age, gender, email, phone, course)
            st.success("✅ Student information updated successfully!")
    else:
        st.info("No students to update.")

# ---------------------------
# Delete Student
# ---------------------------
elif choice == "Delete Student":
    st.subheader("🗑️ Delete Student Record")
    students = get_students()
    if students:
        student_dict = {f"{s[1]} (ID: {s[0]})": s[0] for s in students}
        selected = st.selectbox("Select Student to Delete", list(student_dict.keys()))
        student_id = student_dict[selected]

        if st.button("Delete"):
            delete_student(student_id)
            st.warning("❌ Student record deleted!")
    else:
        st.info("No students to delete.")





# --------- to run ----------------
# streamlit run fashion_registration.py
