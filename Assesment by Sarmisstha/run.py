from app import create_app
from app.db import init_db, load_json_to_db

app = create_app()

if __name__ == "__main__":
    init_db()
    load_json_to_db("data/recipes.json")
    app.run(debug=True)
