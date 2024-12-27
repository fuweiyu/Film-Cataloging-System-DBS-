import mysql.connector

db_config = {
    'host': 'localhost',
    'user': 'collaborator',
    'password': 'dbs2024',
    'database': 'FilmCatalog'
}

try:
    conn = mysql.connector.connect(**db_config)
    print("Connection successful!")
    conn.close()
except mysql.connector.Error as err:
    print(f"Error: {err}")
