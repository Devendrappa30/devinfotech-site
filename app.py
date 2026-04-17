from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

# This ensures the database file path works correctly on Render's Linux servers
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "database.db")

def init_db():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS messages 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT, message TEXT)''')
    conn.commit()
    conn.close()

# CRITICAL FIX: Run the database initialization OUTSIDE the 'if main' block
# This ensures Render creates the database as soon as the app starts.
init_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        msg = request.form['message']
        
        # Use the absolute db_path we defined above
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO messages (name, email, message) VALUES (?, ?, ?)", (name, email, msg))
        conn.commit()
        conn.close()
        return "<h1>Thank you, " + name + "! Your message is saved.</h1><a href='/'>Back Home</a>"
    
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)