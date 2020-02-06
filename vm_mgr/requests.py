from uuid import uuid1
from requests import request, HTTPError

from vm_mgr.application import app


def get_project_token() -> str:
    """
    Get project scoped token suitable for instance creation.

    :return: Admin project token
    """
    token_rq = request(
        method="POST", url=app.config["TOKEN_REF"], json=app.config["TOKEN_BODY"],
    )
    if not token_rq.ok:
        raise HTTPError(token_rq.status_code)

    return token_rq.headers["X-Subject-Token"]


def build_header():
    """
    Small function to build request header
    """
    return {"Content-Type": "application/json", "X-Auth-Token": get_project_token()}


def get_instances() -> dict:
    """
    Make a request to get active instances from devstack.

    :return: dictionary with active machine names and ip addresses
    """
    url = f"{app.config['COMPUTE_SERVERS_REF']}/detail"
    instances_rq = request(
        method="GET", url=url, headers=build_header(), params={"vm_state": "active"},
    )

    if not instances_rq.ok:
        HTTPError(instances_rq.status_code)

    answer = {"servers": list()}
    for instance in instances_rq.json()["servers"]:
        instance_info = dict(name=instance["name"])
        instance_info["ip_addresses"] = list()
        for network, info in instance["addresses"].items():
            instance_info["ip_addresses"].extend(entry["addr"] for entry in info)
        answer["servers"].append(instance_info)

    return answer


def create_instances(flavor: str = None, name: str = None) -> dict:
    """
    Function to make a request to devstack for instance creation.

    :param flavor: preset configuration for instance
    :param name: virtual machine name
    :return: request response
    """
    body = app.config["COMPUTE_CREATE"].copy()
    body["server"]["imageRef"] = get_image_ref()
    body["server"]["flavorRef"] = find_flavor_id(flavor or "m1.nano")

    if name is None:
        name = str(uuid1())

    body["server"]["name"] = name

    create_rq = request(
        method="POST",
        url=app.config["COMPUTE_SERVERS_REF"],
        headers=build_header(),
        json=body,
    )

    if not create_rq.ok:
        raise HTTPError(
            f"Unable to create VM instances: {create_rq.status_code} {create_rq.json()}"
        )
    return create_rq.json()


def get_image_ref() -> str:
    """
    Get imageRef to use it in vm creation request.

    :return: image reference id
    """
    images_rq = request(
        method="GET", url=app.config["IMAGE_REF"], headers=build_header(),
    )
    if not images_rq.ok:
        HTTPError(f"Can not get image id for virtual machine: {images_rq.status_code}")

    [image] = images_rq.json()["images"]
    return image["id"]


def get_flavors() -> dict:
    """
    Get all available flavors

    :return: dictionary with all available flavors
    """
    flavor_rq = request(
        method="GET", url=app.config["FLAVORS_REF"], headers=build_header(),
    )

    if not flavor_rq.ok:
        HTTPError(f"Can not get flavor id for virtual machine: {flavor_rq.status_code}")

    return flavor_rq.json()


def find_flavor_id(flavor_name: str):
    """
    Find flavor id by it's name.

    :param flavor_name: Name of flavor to find id for.
    """
    for flavor in get_flavors()["flavors"]:
        if flavor_name == flavor["name"]:
            return flavor["id"]

    raise AttributeError(f"No flavor '{flavor_name}' found")
