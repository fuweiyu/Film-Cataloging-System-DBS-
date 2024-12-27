from flask import Flask, render_template, request, redirect, flash, session
import mysql.connector
import hashlib  # Import hashlib for hashing

# Flask App Initialization
app = Flask(__name__)
app.secret_key = "your_secret_key"

# Database Configuration
db_config = {
    'host': 'localhost',  # Change this to your MySQL host
    'user': 'collaborator',  # Change this to your MySQL username
    'password': 'dbs2024',  # Change this to your MySQL password
    'database': 'FilmCatalog'  # Change this to your database name
}

# Database Connection
def get_db_connection():
    return mysql.connector.connect(**db_config)

# Login Page
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        # Hash the password using SHA-256
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if the user exists in the PassHash table and whether the password is correct
        cursor.execute("SELECT passwordHash FROM PassHash WHERE userName = %s", (username,))
        result = cursor.fetchone()  # fetchone() returns None if no record is found

        if result and result[0] == hashed_password:
            # Password matches; login successful
            session['username'] = username
            conn.close()
            return redirect("/welcome")
        else:
            # Login failed; username or password incorrect
            flash("Invalid username or password", "danger")
        
        # Close the connection
        cursor.close()
        conn.close()
        
    return render_template("login.html")

# Welcome Page
@app.route("/welcome")
def welcome():
    if 'username' not in session:
        return redirect("/")
    return render_template("welcome.html")

# Logout
@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect("/")

# Signup Page
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        # Hash the password using SHA-256
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Insert new user into the Users and PassHash tables
        try:
            # Insert into Users table
            cursor.execute("INSERT INTO Users (userName, emailAddress, userRole) VALUES (%s, %s, %s)", 
                           (username, f"{username}@example.com", 'normal'))
            # Insert into PassHash table
            cursor.execute("INSERT INTO PassHash (userName, passwordHash) VALUES (%s, %s)", 
                           (username, hashed_password))
            conn.commit()
            flash("Account created successfully! Please log in.", "success")
            return redirect("/")
        except mysql.connector.Error as err:
            if err.errno == mysql.connector.errorcode.ER_DUP_ENTRY:
                flash("Username already exists. Please choose a different username.", "danger")
            else:
                flash(f"Error: {err}", "danger")
        finally:
            # Close the connection
            cursor.close()
            conn.close()
    
    return render_template("signup.html")


if __name__ == "__main__":
    app.run(debug=True)
