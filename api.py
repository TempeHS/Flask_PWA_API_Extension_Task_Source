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
    if request.args.get("lang") and request.args.get("lang").isalpha():
        lang = request.args.get("lang")
        lang = lang.upper()
        api.logger.critical(f"language = {lang}")
        content = dbHandler.extension_get(lang)
    else:
        content = dbHandler.extension_get("*")
    return (content), 200


@api.route("/add_extension", methods=["POST"])
@limiter.limit("1/second", override_defaults=False)
def post():
    data = request.get_json()
    response = dbHandler.extension_add(data)
    return response


if __name__ == "__main__":
    api.run(debug=True, host="0.0.0.0", port=1000)
