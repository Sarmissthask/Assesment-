CREATE TABLE IF NOT EXISTS recipes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cuisine VARCHAR(255),
    title VARCHAR(255),
    rating FLOAT,
    prep_time INT,
    cook_time INT,
    total_time INT,
    description TEXT,
    nutrients JSON,
    serves VARCHAR(50)
);
