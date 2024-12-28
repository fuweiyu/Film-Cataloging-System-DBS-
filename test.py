import mysql.connector

# List of database configurations
db_configs = [
    {
        'host': '172.17.0.2',
        'user': 'FernanShen',
        'password': '012002',
        'database': 'FilmCatalog'
    },
    {
        'host': 'localhost',
        'user': 'collaborator',
        'password': 'dbs2024',
        'database': 'FilmCatalog'
    }
]

# Attempt to connect using each configuration
for config in db_configs:
    try:
        conn = mysql.connector.connect(**config)
        print(f"Connection successful using {config['user']}@{config['host']}!")
        conn.close()
        break  # Exit the loop if the connection is successful
    except mysql.connector.Error as err:
        print(f"Failed to connect using {config['user']}@{config['host']}: {err}")
else:
    print("All connection attempts failed.")
