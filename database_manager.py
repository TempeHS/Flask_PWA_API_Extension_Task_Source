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


# Describe what kind of json you expect.
schema = {
    "type": "object",
    "properties": {
        "extID": {"type": "number"},
        "name": {"type": "string"},
        "hyperlink": {"type": "string"},
        "about": {"type": "string"},
        "image": {"type": "string"},
        "language": {"type": "string"},
    },
}


def extension_add(data):
    validate(instance=data, schema=schema)
    return data
