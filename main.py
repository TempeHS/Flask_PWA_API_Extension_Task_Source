from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
import requests
from flask_wtf import CSRFProtect
from flask_csp.csp import csp_header
import logging


# Code snippet for logging a message
# app.logger.critical("message")


# Generate a basic 16 key: https://acte.ltd/utils/randomkeygen
app = Flask(__name__)
csrf = CSRFProtect(app)
app.secret_key = b"6HlQfWhu03PttohW;apl"


@app.route("/", methods=["GET"])
def root():
    return redirect("/index.html", 302)


@app.route("/index.html", methods=["GET"])
@csp_header(
    {
        "default-src": "'self'",
        "script-src": "'self'",
        "img-src": "http: https: data:",
        "object-src": "'self'",
        "style-src": "'self'",
        "media-src": "'self'",
        "child-src": "'self'",
        "connect-src": "'self'",
        "base-uri": "",
        "report-uri": "/csp_report",
        "frame-ancestors": "none",
    }
)
def index():
    url = "http://127.0.0.1:1000"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
    except requests.exceptions.RequestException as e:
        data = {"error": "Failed to retrieve data from the API"}
    return render_template("index.html", data=data)


@app.route("/privacy.html", methods=["GET"])
def privacy():
    return render_template("/privacy.html")


@app.route("/add.html", methods=["POST", "GET"])
def form():
    if request.method == "POST":
        name = request.form["name"]
        hyperlink = request.form["hyperlink"]
        about = request.form["about"]
        image = request.form["image"]
        language = request.form["language"]
        data = {
            "name": name,
            "hyperlink": hyperlink,
            "about": about,
            "image": image,
            "language": language,
        }
        try:
            response = requests.post("http://127.0.0.1/add_extension", json=data)
            response.raise_for_status()
            return jsonify(response.json()), response.status_code
        except requests.exceptions.RequestException as e:
            return jsonify({"error": str(e)}), 400
        return render_template("/add.html")
    else:
        return render_template("/add.html")


@app.route("/csp_report", methods=["POST"])
def csp_report():
    with open("csp_reports", "a") as fh:
        fh.write(request.data.decode() + "\n")
    return "done"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)