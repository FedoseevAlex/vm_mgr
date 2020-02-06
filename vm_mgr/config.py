import os


SERVER = f"http://{os.environ.get('SERVER_IP')}"

AUTH_REF = f"{SERVER}/identity/v3/auth/tokens"
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

COMPUTE_REF = f"{SERVER}/compute/v2.1"

COMPUTE_SERVERS_REF = f"{COMPUTE_REF}/servers"
COMPUTE_CREATE = {
    "server": {
        "name": "auto-allocate-network",
        "imageRef": None,
        "flavorRef": None,
        "networks": [
            {"uuid": "7eebd447-b45c-4b82-8b1f-5fce8d3330c0"},
            {"uuid": "daae5675-6e78-4251-a17b-5b1c604b5eb2"},
        ],
    }
}

COMPUTE_LIST = {
    "power_state": 1,
    "status": "ACTIVE",
    "vm_state": "ACTIVE",
    "all_tenants": True,
}

FLAVORS_REF = f"{COMPUTE_REF}/flavors"
IMAGE_REF = f"{SERVER}/image/v2/images"
