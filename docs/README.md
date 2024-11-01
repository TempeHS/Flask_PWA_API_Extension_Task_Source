# Flask PWA - API Extension Task

This task is to build a safe API that extends the [Flask PWA - Programming for the Web Task](https://github.com/TempeHS/Flask_PWA_Programming_For_The_Web_Task_Template). From the parent task students will abstract the database and management to an API. The website will then be retooled to GET request the data from the API and POST request data to to API.

## Dependencies

- VSCode, docker, or GitHub Codespaces
- Python 3+
- [SQLite3 Editor](https://marketplace.visualstudio.com/items?itemName=yy0931.vscode-sqlite3-editor)
- [Start git-bash](https://marketplace.visualstudio.com/items?itemName=McCarter.start-git-bash)
- [Thunder Client](https://marketplace.visualstudio.com/items?itemName=rangav.vscode-thunder-client)
- pip installs (or pip3 if macOS)

```bash
    pip install Flask
    pip install SQLite3
    pip install flask_wtf
    pip install flask_csp
    pip install jsonschema
```

> [!Note]
> These instructions are not as verbose as the parent task because students are expected to be familiar with Bash, Flask & SQLite3

## Instructions

### Step 1: Learn the basics of implementing an API in Flask

Watch: [Build a Flask API in 12 Minutes](https://www.youtube.com/watch?v=zsYIw6RXjfM)

### Step 2: Create the Directory Structure

```text
├── .database
│   ├── data_source.db
│   └── my_queries.sqlite3-query
├── .workingdocuments
├── static
│   ├── css
│   │   ├──bootstrap.min.css
│   │   └──style.css
│   ├── icons
│   ├── images
│   │   ├──favicon.png
│   │   └──logo.png
│   └── js
│   │   ├──app.js
│   │   ├──bootstrap.bundle.min.js
│   │   └──serviceWorker.js
├── templates
├── LICENSE
├── api.py
├── app.py
└── database_manager.py
```

### Step 3 setup a basic API in api.py

This Python implementation:

1. Imports all the required dependencies
2. Configures the logger to log to api_security_log.log\
3. Configures the 'Cross Origin Request policy
4. Configures the rate limiter
5. Sets a API route GET method to return a string and 200 response
6. Sets a API route POST method to return the POST data and a 201 response

```python
from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS, cross_origin
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging

import database_manager as dbHandler


app_log = logging.getLogger(__name__)
logging.basicConfig(
    filename="api_security_log.log",
    encoding="utf-8",
    level=logging.DEBUG,
    format="%(asctime)s %(message)s",
)


api = Flask(__name__)
cors = CORS(api)
api.config["CORS_HEADERS"] = "Content-Type"
limiter = Limiter(
    get_remote_address,
    app=api,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)


@api.route("/", methods=["GET"])
@limiter.limit("1/second", override_defaults=False)
def get():
    return ("API Works"), 200


@api.route("/add_extension", methods=["POST"])
@limiter.limit("1/second", override_defaults=False)
def post():
    data = request.get_json()
    return data, 201


if __name__ == "__main__":
    api.run(debug=True, host="0.0.0.0", port=1000)
```

### Step 3: Test your basic API with Thunder Client

![Screen recording testing an API with Thunder Client](README_resources\test_basic_API.gif "Follow these steps to test your basic API")

### Step 4: Build a basic GET response

Extend the GET request in `api.py` to get data from the database from the bdHandler and return it to the request with the status `200`.

```python
def get():
    content = dbHandler.extension_get("*")
    return (content), 200
```

Implement a database query that returns JSON data in `database_manager.py` to the request GET method that:

1. Imports all the required dependencies
2. Connects to the SQLite3 database
3. Executes a query
4. Converts the query data to a JSON structure
5. Returns the JSON data

```python
from flask import jsonify
import sqlite3 as sql
import json
from jsonschema import validate


def extension_get():
    con = sql.connect(".database/data_source.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM extension")
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

```

### Step 5: Test your basic GET Response

![Screen recording testing a API GET with Thunder Client](README_resources\test_basic_GET_API.gif "Follow these steps to test your basic GET API")

### Step 6 Add a language argument to filter extensions by language

Extend the GET request in `api.py` to either get all data or data that matches a language parameter from the database that

1. Validating the argument is "lang" and that the "lang" is only alpha characters for security
2. Passing the language request to the dbHandler
3. Return the data from dbHandler to the request
4. return the status `200`

```python
def get():
    # For security data is validated on entry
    if request.args.get("lang") and request.args.get("lang").isalpha():
        lang = request.args.get("lang")
        lang = lang.upper()
        api.logger.critical(f"language = {lang}")
        content = dbHandler.extension_get(lang)
    else:
        content = dbHandler.extension_get("*")
    return (content), 200
```

Extend the database query to filter the SQL query based on the argument parameter and return it as JSON data to the request GET method that:

1. If no parameter or a invalid parameter is passed the function will return the entire database in a JSON format.
2. If a valid parameter is passed the database will be queried with with a LIKE and all matching (if any) will be returned

```python
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
```

### Step 7: Test your GET Response

![Screen recording testing a API GET with Thunder Client](README_resources\test_GET_API.gif "Follow these steps to test your GET API")

### Step 8: Setup your basic POST response

Extend /add_extension POST request to pass the POST data to teh DB Handler and return the response with a 201 status code.

```python
def post():
    data = request.get_json()
    response = dbHandler.extension_add(data)
    return response, 201
```

Extend the dbHandler to pass the data back to the POST request.

```python
def extension_add(response):
    data = response
    return data
```

### Step 9: Test your basic POST response

![Screen recording testing a API basic POST with Thunder Client](README_resources\test_basic_POST_API.gif "Follow these steps to test your basic POST API")

```text
{"extID": 4, "name": "test", "hyperlink": "http://test", "about": "This is a test", "image": "http://test.jpg", "language": "TEST"}
```
