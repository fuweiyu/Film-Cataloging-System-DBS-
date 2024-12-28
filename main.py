from flask import Flask, render_template, request, redirect, flash, session
import mysql.connector
import hashlib  # for SHA-256 hashing

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Replace with a secure, random value

# List of database configurations
db_configs = [
    {
        'host': '172.17.0.2',     # Fallback host
        'user': 'FernanShen',     # Fallback username
        'password': '012002',     # Fallback password
        'database': 'FilmCatalog' # Fallback database name
    },
    {
        'host': 'localhost',     # Change to your MySQL host
        'user': 'collaborator',  # Change to your MySQL username
        'password': 'dbs2024',   # Change to your MySQL password
        'database': 'FilmCatalog'# Change to your database name
    }
]

# Helper function to get a DB connection
def get_db_connection():
    for config in db_configs:
        try:
            connection = mysql.connector.connect(**config)
            print(f"Connected to database using {config['user']}@{config['host']}")
            return connection
        except mysql.connector.Error as err:
            print(f"Failed to connect using {config['user']}@{config['host']}: {err}")
    raise Exception("All database connection attempts failed.")

# ----------------------------------
# USER INJECTOR
# ----------------------------------
@app.context_processor
def inject_user():
    is_logged_in = 'user_id' in session
    username = session.get('username', "Guest")
    return {'is_logged_in': is_logged_in, 'username': username}



#----------------------------------
# MAIN PAGE
# ----------------------------------
@app.route("/")
def main_page():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Generate random movies for each tab
    tabs = []
    num_tabs = 5  # Number of tabs
    for _ in range(num_tabs):
        cursor.execute("""
            SELECT movieId, title, overview
            FROM Movies
            ORDER BY RAND()
            LIMIT 10;
        """)
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

        # Hash the password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        conn = get_db_connection()
        cursor = conn.cursor()

        # Check user credentials
        cursor.execute("""
            SELECT userId, userName FROM Users WHERE userName = %s OR emailAddress = %s
        """, (username_or_email, username_or_email))
        user_row = cursor.fetchone()

        if not user_row:
            flash("Invalid username/email or password", "danger")
            cursor.close()
            conn.close()
            return redirect("/login")

        user_id, username = user_row

        # Validate password
        cursor.execute("SELECT passwordHash FROM UserPasswords WHERE userId = %s", (user_id,))
        pass_row = cursor.fetchone()

        if pass_row and pass_row[0] == hashed_password:
            session['user_id'] = user_id
            session['username'] = username  # Store username only when logged in
            session.permanent = True
            #flash("Welcome back!", "success") #turned into comment 
            cursor.close()
            conn.close()
            return redirect("/")
        else:
            flash("Invalid username/email or password", "danger")

        cursor.close()
        conn.close()

    return render_template("login.html")


# ----------------------------------
# LOGOUT
# ----------------------------------
@app.route("/logout")
def logout():
    """
    Logs out the current user by clearing the session.
    """
    session.pop('username', None)
    #flash("You have been logged out.", "info")
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

# FERNAN MODIFICO ESTA PARTE
# ----------------------------------
# SEARCH
# ----------------------------------
@app.route("/search", methods=["GET"])
def search():
    # Check if the user is logged in
    is_logged_in = 'user_id' in session
    username = session.get('username')

    query = request.args.get("query", "").strip()
    if not query:
        flash("Please enter a search term.", "warning")
        return redirect("/")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Search for movies by title
    search_query = f"%{query}%"
    cursor.execute("""
        SELECT DISTINCT Movies.movieId, Movies.title, Movies.overview
        FROM Movies
        WHERE Movies.title LIKE %s
    """, (search_query,))
    title_matches = cursor.fetchall()

    # Search for movies by keywords
    cursor.execute("""
        SELECT DISTINCT Movies.movieId, Movies.title, Movies.overview
        FROM Movies
        JOIN MovieKeywords ON Movies.movieId = MovieKeywords.movieId
        JOIN Keywords ON MovieKeywords.keywordId = Keywords.keywordId
        WHERE Keywords.name LIKE %s
    """, (search_query,))
    keyword_matches = cursor.fetchall()

    cursor.close()
    conn.close()

    # Remove duplicates (if a movie matches both title and keyword)
    movie_ids = set()
    combined_results = []
    for movie in title_matches + keyword_matches:
        if movie["movieId"] not in movie_ids:  # Use movieId instead of id
            movie_ids.add(movie["movieId"])
            combined_results.append(movie)
            

    return render_template("search.html", query=query, search_results=combined_results, title_matches=title_matches, keyword_matches=keyword_matches, is_logged_in=is_logged_in, username=username)

# ----------------------------------
# MOVIE DETAILS
# ----------------------------------
@app.route("/movie/<int:movie_id>", methods=["GET", "POST"])
def movie_detail(movie_id):
    # Check if user is logged in
    is_logged_in = 'user_id' in session
    username = session.get('username')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch movie details
    cursor.execute("""
        SELECT movieId, title, tagline, overview, releaseDate, language, runtime, budget
        FROM Movies
        WHERE movieId = %s
    """, (movie_id,))
    movie = cursor.fetchone()

    if not movie:
        cursor.close()
        conn.close()
        flash("Movie not found!", "danger")
        return redirect("/search")

    # Handle comment submission
    if request.method == "POST":
        user_id = session.get("user_id")
        comment_text = request.form.get("comment")

        # Debugging logs
        print("User ID:", user_id)
        print("Comment Text:", comment_text)

        if not user_id:
            flash("You need to be logged in to post comments.", "warning")
            return redirect("/login")

        if comment_text.strip():
            cursor.execute("""
                INSERT INTO Comments (movieId, userId, commentText)
                VALUES (%s, %s, %s)
            """, (movie_id, user_id, comment_text.strip()))
            conn.commit()
            flash("Your comment was posted successfully!", "success")
        #else:
            #flash("Comment cannot be empty.", "danger")

    # Fetch comments for the movie
    cursor.execute("""
        SELECT c.commentText, c.timeStamp, u.userName
        FROM Comments c
        JOIN Users u ON c.userId = u.userId
        WHERE c.movieId = %s
        ORDER BY c.timeStamp DESC
    """, (movie_id,))
    comments = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("movie.html", movie=movie, comments=comments, is_logged_in=is_logged_in, username=username)

# ----------------------------------
# MAIN
# ----------------------------------
if __name__ == "__main__":
    app.run(debug=True)
