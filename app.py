from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

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
# Home Page (Form)
# -------------------------------
@app.route('/')
def home():
    return render_template('form.html')


# -------------------------------
# Submit Form Data
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

    return redirect('/')


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
# Delete Single Row
# -------------------------------
@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM users WHERE id = ?", (id,))

    conn.commit()

    # 🔥 Reset ID if table becomes empty
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]

    if count == 0:
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='users'")

    conn.commit()
    conn.close()

    return redirect('/view')


# -------------------------------
# Delete All Data (Optional)
# -------------------------------
@app.route('/delete_all')
def delete_all():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM users")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='users'")

    conn.commit()
    conn.close()

    return redirect('/view')


# -------------------------------
# Run App
# -------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)