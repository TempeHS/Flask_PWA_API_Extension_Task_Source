from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask_wtf import CSRFProtect
from flask_csp.csp import csp_header
import logging


# app_log = logging.getLogger(__name__)
# logging.basicConfig(
#    filename="app_security_log.log",
#     encoding="utf-8",
#    level=logging.DEBUG,
#    format="%(asctime)s %(message)s",
# )


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
    return render_template("/index.html")


@app.route("/privacy.html", methods=["GET"])
def privacy():
    return render_template("/privacy.html")


@app.route("/add.html", methods=["POST", "GET"])
def form():
    if request.method == "POST":
        email = request.form["email"]
        text = request.form["text"]
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
