import sqlite3

# Connect to database
conn = sqlite3.connect('database.db')

# Execute SQL commands from the SQL script
with open('init_db.sql', 'r') as f:
    conn.executescript(f.read())

# Close connection
conn.close()
