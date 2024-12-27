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

#----------------------------------
# MAIN PAGE
# ----------------------------------
@app.route("/")
def main_page():
    """
    Main page with tabs displaying lists of random movies.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Generate random movies for each tab
    tabs = []
    num_tabs = 5  # Number of tabs
    for _ in range(num_tabs):
        cursor.execute("SELECT title, overview FROM Movies ORDER BY RAND() LIMIT 10;")
        tabs.append(cursor.fetchall())

    cursor.close()
    conn.close()

    # Check if the user is logged in and pass username to template
    is_logged_in = 'username' in session
    username = session['username'] if is_logged_in else None

    return render_template("main.html", tabs=tabs, is_logged_in=is_logged_in, username=username)

# ----------------------------------
# LOGIN
# ----------------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username_or_email = request.form['username_or_email']
        password = request.form['password']

        # Hash the incoming password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        conn = get_db_connection()
        cursor = conn.cursor()

        # Check for username or email match in Users table
        cursor.execute("""
            SELECT userId FROM Users WHERE userName = %s OR emailAddress = %s
        """, (username_or_email, username_or_email))
        user_row = cursor.fetchone()

        if not user_row:
            flash("Invalid username/email or password", "danger")
            cursor.close()
            conn.close()
            return redirect("/login")

        user_id = user_row[0]

        # Validate the password from UserPasswords table
        cursor.execute("SELECT passwordHash FROM UserPasswords WHERE userId = %s", (user_id,))
        pass_row = cursor.fetchone()

        if pass_row and pass_row[0] == hashed_password:
            # Successful login
            session['username'] = username_or_email  # Store username or email in session
            flash("Welcome back!", "success")
            cursor.close()
            conn.close()
            return redirect("/")
        else:
            flash("Invalid username/email or password", "danger")

        cursor.close()
        conn.close()

    return render_template("login.html")

# ----------------------------------
# WELCOME
# ----------------------------------
@app.route("/welcome")
def welcome():
    """
    Simple welcome page after successful login.
    """
    if 'username' not in session:
        return redirect("/")
    return render_template("welcome.html")


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
# SIGNUP
# ----------------------------------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Hash the password using SHA-256
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            # Check if the username or email already exists
            cursor.execute("""
                SELECT userName, emailAddress FROM Users WHERE userName = %s OR emailAddress = %s
            """, (username, email))
            existing_user = cursor.fetchone()

            if existing_user:
                # Only trigger the appropriate message
                if existing_user[0] == username and existing_user[1] == email:
                    flash("Username and email already exist. Please use different ones.", "danger")
                elif existing_user[0] == username:
                    flash("Username already exists. Please choose a different one.", "danger")
                elif existing_user[1] == email:
                    flash("Email already exists. Please use a different email.", "danger")
                
                # Stop further execution
                return redirect("/signup")

            # Insert new user into Users table
            cursor.execute("""
                INSERT INTO Users (userName, emailAddress, userRole)
                VALUES (%s, %s, %s)
            """, (username, email, 'normal'))

            # Get the auto-incremented userId
            new_user_id = cursor.lastrowid

            # Insert into UserPasswords table
            cursor.execute("""
                INSERT INTO UserPasswords (userId, passwordHash)
                VALUES (%s, %s)
            """, (new_user_id, hashed_password))

            conn.commit()

            # Flash success message and redirect to login
            flash("Account created successfully! Please log in.", "success")
            return redirect("/login")

        except mysql.connector.Error as err:
            flash(f"Database error: {err}", "danger")

        finally:
            cursor.close()
            conn.close()

    return render_template("signup.html")

# ----------------------------------
# MAIN
# ----------------------------------
if __name__ == "__main__":
    app.run(debug=True)