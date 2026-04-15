from flask import Flask, render_template, request, redirect, flash
import sqlite3

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = 'secret123'   # 🔥 Needed for flash messages

# -------------------------------
# Initialize Database
# -------------------------------
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            message TEXT
        )
    ''')

    conn.commit()
    conn.close()


# -------------------------------
# Home Page
# -------------------------------
@app.route('/')
def home():
    return render_template('form.html')


# -------------------------------
# Submit Form
# -------------------------------
@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO users (name, email, message) VALUES (?, ?, ?)",
        (name, email, message)
    )

    conn.commit()
    conn.close()

    flash("Data submitted successfully!")   # ✅ Success message
    return redirect('/')   # ✅ Stay on form


# -------------------------------
# View Data
# -------------------------------
@app.route('/view')
def view():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()

    conn.close()
    return render_template('view.html', data=rows)


# -------------------------------
# Delete
# -------------------------------
@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM users WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return redirect('/')


# -------------------------------
# Run App
# -------------------------------
if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=10000)