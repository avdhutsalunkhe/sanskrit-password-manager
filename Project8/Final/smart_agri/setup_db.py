import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()

c.execute('''
  CREATE TABLE IF NOT EXISTS farmer (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT UNIQUE,
    password TEXT,
    region TEXT
  )
''')

conn.commit()
conn.close()
