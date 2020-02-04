import os
from ipaddress import IPv4Address

AUTH_REF = f"http://{os.environ.get('SERVER_IP')}/identity/v3/auth/tokens"
AUTH_BODY = {
    "auth": {
        "identity": {
            "methods": ["password"],
            "password": {
                "user": {
                    "name": os.environ.get("AUTH_NAME"),
                    "domain": {"name": "Default"},
                    "password": os.environ.get("AUTH_PASSWORD"),
                }
            },
        }
    }
}
