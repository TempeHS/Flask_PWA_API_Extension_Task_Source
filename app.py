from flask import Flask
from flask import redirect
from flask import render_template
import requests
from flask_wtf import CSRFProtect
from flask_csp.csp import csp_header
import logging


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
    response = requests.get(url)
    data = response.json()
    return render_template("/index.html", data=data)


@app.route("/privacy.html", methods=["GET"])
def privacy():
    return render_template("/privacy.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
