from flask import Blueprint, request, render_template, redirect, url_for, flash
import mysql.connector
from werkzeug.security import generate_password_hash  # 1. Import hashing utility

auth = Blueprint('auth', __name__)

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_password",
        database="Fixtrace_db"
    )

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        role = request.form.get('role', 'Customer') # Default to Customer if not provided
        
        # 2. Hash password securely before database insertion
        hashed_password = generate_password_hash(password)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            # 3. Use parameterized queries (%s) to prevent SQL injection
            query = "INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (name, email, hashed_password, role))
            
            # 4. Commit changes so they actually save to MySQL
            conn.commit()
            
            return redirect(url_for('auth.login')) # Redirect to login after success
            
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return "Registration failed. Email might already exist.", 400
            
        finally:
            # 5. Always close connections to avoid memory leaks
            cursor.close()
            conn.close()
            
    # 6. Handles the 'GET' request (when a user just visits the page)
    return render_template('register.html')