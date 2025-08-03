-- init_db.sql
CREATE TABLE IF NOT EXISTS predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    n REAL,
    p REAL,
    k REAL,
    temp REAL,
    humidity REAL,
    ph REAL,
    rainfall REAL,
    crop TEXT
);
