from typing import Dict

from flask import Flask
from requests import request, Response

app = Flask(__name__)
app.config.from_pyfile("config.py")


@app.route("/auth", methods=["POST"])
def authentication() -> Response:
    """
    Authenticate itself to devstack

    :return: Dict containing token information
    """
    result = request(
        method="POST", url=app.config["AUTH_REF"], json=app.config["AUTH_BODY"]
    )
    return result


if __name__ == "__main__":
    pass
