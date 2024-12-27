from flask import Flask, render_template, request, redirect, flash, session
import mysql.connector
import hashlib  # for SHA-256 hashing

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Replace with a secure, random value

# Database Configuration
db_config = {
    'host': 'localhost',       # Change to your MySQL host
    'user': 'collaborator',    # Change to your MySQL username
    'password': 'dbs2024',     # Change to your MySQL password
    'database': 'FilmCatalog'  # Change to your database name
}

# Helper function to get a DB connection
def get_db_connection():
    return mysql.connector.connect(**db_config)

# ----------------------------------
# MAIN PAGE
# ----------------------------------
@app.route("/")
def main_page():
    """
    Default main page showing the movie catalog.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT title, overview FROM Movies ORDER BY RAND() LIMIT 10;"
    cursor.execute(query)
    movies = cursor.fetchall()
    cursor.close()
    conn.close()

    # Check if the user is logged in and pass username to template
    is_logged_in = 'username' in session
    username = session['username'] if is_logged_in else None

    return render_template("main.html", movies=movies, is_logged_in=is_logged_in, username=username)

# ----------------------------------
# LOGIN
# ----------------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Login route:
    User provides username + password, which are validated against the database.
    """
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        # Hash the incoming password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        conn = get_db_connection()
        cursor = conn.cursor()

        # Step 1: Get userId from Users
        cursor.execute("SELECT userId FROM Users WHERE userName = %s", (username,))
        user_row = cursor.fetchone()

        if not user_row:
            # userName not found
            flash("Invalid username or password", "danger")
            cursor.close()
            conn.close()
            return redirect("/login")

        user_id = user_row[0]

        # Step 2: Use userId to get passwordHash from UserPasswords
        cursor.execute("SELECT passwordHash FROM UserPasswords WHERE userId = %s", (user_id,))
        pass_row = cursor.fetchone()

        if pass_row and pass_row[0] == hashed_password:
            # Successful login
            session['username'] = username
            flash("Welcome back!", "success")
            cursor.close()
            conn.close()
            return redirect("/")
        else:
            # Password does not match or no record in UserPasswords
            flash("Invalid username or password", "danger")

        cursor.close()
        conn.close()

    return render_template("login.html")

# ----------------------------------
# SIGNUP
# ----------------------------------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    """
    Signup route:
    New users can create an account, and their credentials are saved in the database.
    """
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        # Hash the password using SHA-256
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            # 1) Insert into Users table
            cursor.execute("""
                INSERT INTO Users (userName, emailAddress, userRole)
                VALUES (%s, %s, %s)
            """, (username, f"{username}@example.com", 'normal'))
            
            # 2) Get the auto-incremented userId
            new_user_id = cursor.lastrowid

            # 3) Insert into UserPasswords
            cursor.execute("""
                INSERT INTO UserPasswords (userId, passwordHash)
                VALUES (%s, %s)
            """, (new_user_id, hashed_password))

            conn.commit()
            flash("Account created successfully! Please log in.", "success")
            return redirect("/login")

        except mysql.connector.Error as err:
            # Handle duplicate entries or other SQL errors
            if err.errno == mysql.connector.errorcode.ER_DUP_ENTRY:
                flash("Username already exists. Please choose a different username.", "danger")
            else:
                flash(f"Error: {err}", "danger")

        finally:
            cursor.close()
            conn.close()

    return render_template("signup.html")

# ----------------------------------
# LOGOUT
# ----------------------------------
@app.route("/logout")
def logout():
    """
    Logs out the current user by clearing the session.
    """
    session.pop('username', None)
    flash("You have been logged out.", "info")
    return redirect("/")

# ----------------------------------
# RUN THE APPLICATION
# ----------------------------------
if __name__ == "__main__":
    app.run(debug=True)

