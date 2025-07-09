from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flashing messages


# ---------- Database Setup ----------
def init_db():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            email TEXT,
            course TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()


# ---------- Routes ----------

# Home - View all students
@app.route('/home')
def home():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM students")
    students = cur.fetchall()
    conn.close()
    return render_template('home.html', students=students)



# Add Student
@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        email = request.form['email']
        course = request.form['course']

        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute("INSERT INTO students (name, age, email, course) VALUES (?, ?, ?, ?)",
                    (name, age, email, course))
        conn.commit()
        conn.close()
        flash('Student added successfully!')
        return redirect(url_for('index'))

    return render_template('add.html')


# Edit Student
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        email = request.form['email']
        course = request.form['course']
        cur.execute("UPDATE students SET name=?, age=?, email=?, course=? WHERE id=?",
                    (name, age, email, course, id))
        conn.commit()
        conn.close()
        flash('Student updated successfully!')
        return redirect(url_for('index'))

    cur.execute("SELECT * FROM students WHERE id=?", (id,))
    student = cur.fetchone()
    conn.close()
    return render_template('edit.html', student=student)


# Delete Student
# Show confirmation page
@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete_student(id):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    if request.method == 'POST':
        cur.execute("DELETE FROM students WHERE id=?", (id,))
        conn.commit()
        conn.close()
        flash('Student deleted successfully!')
        return redirect(url_for('index'))

    cur.execute("SELECT * FROM students WHERE id=?", (id,))
    student = cur.fetchone()
    conn.close()
    return render_template('delete.html', student=student)



# Search Students
@app.route('/search', methods=['GET', 'POST'])
def search_student():
    students = []
    if request.method == 'POST':
        keyword = request.form['keyword']
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM students WHERE name LIKE ? OR course LIKE ?",
                    ('%' + keyword + '%', '%' + keyword + '%'))
        students = cur.fetchall()
        conn.close()
    return render_template('search.html', students=students)


# View Student Details
@app.route('/student/<int:id>')
def student_detail(id):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM students WHERE id=?", (id,))
    student = cur.fetchone()
    conn.close()
    return render_template('student_detail.html', student=student)


# About Page
@app.route('/about')
def about():
    return render_template('about.html')


# Contact Page
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        # You can add logic here to save to a database or send via email
        flash('Thank you for your message! We will get back to you soon.')
        return redirect(url_for('contact'))

    return render_template('contact.html')



# Login Page (optional)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # TODO: Replace with actual user authentication logic
        if email == "admin@example.com" and password == "admin123":
            flash('Login successful!')
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials. Please try again.')

    return render_template('login.html')



# Register Page (optional)
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm = request.form['confirm']

        if password != confirm:
            flash('Passwords do not match!')
            return redirect(url_for('register'))

        # TODO: Add database logic to store user info
        flash('Registration successful!')
        return redirect(url_for('login'))

    return render_template('register.html')

 # Root route that redirects to home
@app.route('/')
def index():
    return redirect(url_for('home'))

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
