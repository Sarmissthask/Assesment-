from flask import Blueprint, request, jsonify
import sqlite3, json

routes = Blueprint("routes", __name__)

def get_db():
    return sqlite3.connect("recipes.db")

# -------------------------------
# API 1: Get All Recipes
# -------------------------------
@routes.route("/api/recipes", methods=["GET"])
def get_all_recipes():
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))
    offset = (page - 1) * limit

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM recipes")
    total = cur.fetchone()[0]

    cur.execute("""
        SELECT * FROM recipes
        ORDER BY rating DESC
        LIMIT ? OFFSET ?
    """, (limit, offset))

    rows = cur.fetchall()
    conn.close()

    data = []
    for r in rows:
        data.append({
            "id": r[0],
            "cuisine": r[1],
            "title": r[2],
            "rating": r[3],
            "prep_time": r[4],
            "cook_time": r[5],
            "total_time": r[6],
            "description": r[7],
            "nutrients": json.loads(r[8]),
            "serves": r[9]
        })

    return jsonify({
        "page": page,
        "limit": limit,
        "total": total,
        "data": data
    })


# -------------------------------
# API 2: Search Recipes
# -------------------------------
@routes.route("/api/recipes/search", methods=["GET"])
def search_recipes():
    title = request.args.get("title")
    cuisine = request.args.get("cuisine")
    rating = request.args.get("rating")
    total_time = request.args.get("total_time")
    calories = request.args.get("calories")

    query = "SELECT * FROM recipes WHERE 1=1"
    params = []

    if title:
        query += " AND title LIKE ?"
        params.append(f"%{title}%")

    if cuisine:
        query += " AND cuisine = ?"
        params.append(cuisine)

    if rating:
        query += f" AND rating {rating}"

    if total_time:
        query += f" AND total_time {total_time}"

    if calories:
        query += f" AND json_extract(nutrients, '$.calories') {calories}"

    conn = get_db()
    cur = conn.cursor()
    cur.execute(query, params)
    rows = cur.fetchall()
    conn.close()

    data = []
    for r in rows:
        data.append({
            "id": r[0],
            "title": r[2],
            "cuisine": r[1],
            "rating": r[3],
            "total_time": r[6],
            "nutrients": json.loads(r[8]),
            "serves": r[9]
        })

    return jsonify({"data": data})
