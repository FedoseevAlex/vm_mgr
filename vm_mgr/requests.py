from requests import request, HTTPError

from vm_mgr.application import app


def auth() -> str:
    """
    Authenticate to devstack

    :return: Token to use in requests
    """
    token_rq = request(
        method="POST", url=app.config["AUTH_REF"], json=app.config["AUTH_BODY"],
    )
    if not token_rq.ok:
        raise HTTPError(token_rq.status_code)

    print(token_rq.headers["X-Subject-Token"])
    return token_rq.headers["X-Subject-Token"]


def build_header():
    return {"Content-Type": "application/json", "X-Auth-Token": auth()}


def get_instances() -> dict:
    """
    Make a request to get active instances from devstack.
    """
    instances_rq = request(
        method="GET",
        url=app.config["COMPUTE_SERVERS_REF"],
        headers=build_header(),
        json=app.config["COMPUTE_LIST"],
    )

    if not instances_rq.ok:
        HTTPError(instances_rq.status_code)

    return instances_rq.json()


def create_instances():
    """
    Function to make a request to devstack for instance creation.

    :param options: Container for additional settings for virtual machines
    """
    create_rq = request(
        method="POST",
        url=app.config["COMPUTE_REF"],
        headers=build_header(),
        json=app.config["COMPUTE_LIST"],
    )


def get_image_ref():
    """
    Get imageRef to use it in vm creation request.
    """
    images_rq = request(
        method="GET", url=app.config["IMAGE_REF"], headers=build_header(),
    )
    if not images_rq.ok:
        HTTPError(f"Can not get image id for virtual machine: {images_rq.status_code}")

    return images_rq.json()

def get_flavors():
    """
    Get all available flavors
    """
    flavor_rq = request(
        method="GET", url=app.config["FLAVORS_REF"], headers=build_header(),
    )

    if not flavor_rq.ok:
        HTTPError(f"Can not get flavor id for virtual machine: {flavor_rq.status_code}")

    return flavor_rq.json()


def find_nano_flavor(flavors):
    """
    Find m1.nano flavor id
    """
    for flavor in flavors:
        if 'm1.nano' == flavor["name"]:
            return flavor["id"]

    raise AttributeError('No flavor m1.nano found')
