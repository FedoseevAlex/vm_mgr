import os


SERVER = f"http://{os.environ.get('SERVER_IP')}"

ADMIN_PROJECT_ID = "21f230e839624efc965c9008128fa194"
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
        "scope": {"project": {"id": ADMIN_PROJECT_ID}},
    }
}


COMPUTE_REF = f"{SERVER}/compute/v2.1"

COMPUTE_SERVERS_REF = f"{COMPUTE_REF}/servers"
COMPUTE_CREATE = {
    "server": {
        "name": "auto-allocate-network",
        "imageRef": None,
        "flavorRef": 42,
        "networks": [{"uuid": "7eebd447-b45c-4b82-8b1f-5fce8d3330c0"},],
    }
}

FLAVORS_REF = f"{COMPUTE_REF}/flavors"
IMAGE_REF = f"{SERVER}/image/v2/images"
