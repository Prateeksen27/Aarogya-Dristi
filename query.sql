CREATE TABLE patient (
    name TEXT,
    age TEXT,
    gender TEXT,
    email TEXT PRIMARY KEY NOT NULL UNIQUE,
    password TEXT
);
