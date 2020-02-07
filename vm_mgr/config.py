import os


SERVER = f"http://{os.environ.get('SERVER_IP')}"

TOKEN_REF = f"{SERVER}/identity/v3/auth/tokens"
TOKEN_BODY = {
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
        },
    }
}

PROJECTS_REF = f"{SERVER}/identity/v3/auth/projects"

COMPUTE_REF = f"{SERVER}/compute/v2.1"

COMPUTE_SERVERS_REF = f"{COMPUTE_REF}/servers"
COMPUTE_CREATE = {
    "server": {
        "name": "auto-allocate-network",
        "imageRef": None,
        "flavorRef": 42,
        "networks": None,
    }
}

FLAVORS_REF = f"{COMPUTE_REF}/flavors"
IMAGE_REF = f"{SERVER}/image/v2/images"
