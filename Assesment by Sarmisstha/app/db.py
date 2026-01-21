import sqlite3
import json
import math

DB_NAME = "recipes.db"

def get_db():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute(open("schema.sql").read())
    conn.commit()
    conn.close()

def clean_number(value):
    try:
        if value is None:
            return None
        if isinstance(value, float) and math.isnan(value):
            return None
        return value
    except:
        return None

def load_json():
    conn = get_db()
    cur = conn.cursor()

    with open("data/recipes.json", encoding="utf-8") as f:
        recipes = json.load(f)

    for r in recipes:
        cur.execute("""
        INSERT INTO recipes (
            cuisine, title, rating, prep_time,
            cook_time, total_time, description,
            nutrients, serves
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            r.get("cuisine"),
            r.get("title"),
            clean_number(r.get("rating")),
            clean_number(r.get("prep_time")),
            clean_number(r.get("cook_time")),
            clean_number(r.get("total_time")),
            r.get("description"),
            json.dumps(r.get("nutrients")),
            r.get("serves")
        ))

    conn.commit()
    conn.close()
