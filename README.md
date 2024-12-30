# Film-Cataloging-System-DBS
資料庫系統概論的期末專題
Introduction to Database Systems' Final Project

![Alt Text](static/nycuflix.png)

## How to run the Application


1. Activate the environment 
```
source myenv/bin/activate
```
2. Requirements:
Install mysql connector (ubuntu)
```
pip install flask mysql-connector-python
```
3. Set up the database
open MySQL:
```
sudo mysql -u root -p
```
Create and populate the database
```
sql> SOURCE /your-path/Film-Cataloging-System-DBS-/queries/DBcreation.sql;
sql> SOURCE /your-path/Film-Cataloging-System-DBS-/queries/DBpopulation.sql;
```
Note: The csv files must be in the specified path for mySQL to be able to load it 

Create and grant privileges to the user whose credentials are used for the database connection:
```
CREATE USER 'collaborator'@'localhost' IDENTIFIED BY 'dbs2024';
GRANT ALL PRIVILEGES ON FilmCatalog.* TO 'collaborator'@'localhost';
FLUSH PRIVILEGES;
```
4. Run the python script
```
python3 main.py
```
4. Go to the link provided in the console
### main.py
The primary backend script for the application, built using Flask. It manages routes, user authentication, movie data retrieval, and CRUD operations. Also handles database connections using MySQL.
- Key Features:
	- User login and signup functionalities.
	- Movie listing, search, and rating features.
	- Admin dashboard for managing movie data.

### Queries Folder
- DBcreation.sql
SQL script to create the database schema for the Film Cataloging System. Defines tables such as `Movies`, `Users`, `Comments`, `Ratings`, and others required for the system.

-  DBpopulation.sql
 SQL script to populate the database with initial data for testing and development. Includes sample movies, users, and other necessary records.

### Static Folder
Folder which contains images to display in the design of the page

### Templates folder
- admin_dashboard.html
- login.html
- signup.html
- search.html
- movie.html

### myenv folder
Environment folder containing dependencies and configurations for running the Flask app. 
