from flask import jsonify
import sqlite3 as sql
import json
from jsonschema import validate


def extension_get(lang):
    con = sql.connect(".database/data_source.db")
    cur = con.cursor()
    if lang == "*":
        cur.execute("SELECT * FROM extension")
    else:
        cur.execute("SELECT * FROM extension WHERE language LIKE ?;", [lang])
    migrate_data = [
        dict(
            extID=row[0],
            name=row[1],
            hyperlink=row[2],
            about=row[3],
            image=row[4],
            language=row[5],
        )
        for row in cur.fetchall()
    ]
    return jsonify(migrate_data)


def extension_add():
    data = request.get_json()
    info = dict(request.headers)
    api.logger.critical(f"User {info}")
    api.logger.critical(f"Has added the movie {data}")
    dbHandler.add_film(data)
    return data, 201


# Describe what kind of json you expect.
schema = {
    "type": "object",
    "properties": {
        "extID": {"type": "number"},
        "name": {"type": "string"},
        "about": {"type": "string"},
        "image": {"type": "string"},
        "image": {"type": "string"},
    },
}

# Convert json to python object.
my_json = json.loads(
    '{"description": "Hello world!", "status": true, "value_a": 1, "value_b": 3.14}'
)

# Validate will raise exception if given json is not
# what is described in schema.
validate(instance=my_json, schema=schema)
