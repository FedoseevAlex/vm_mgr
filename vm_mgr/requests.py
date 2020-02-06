from uuid import uuid1
from requests import request, HTTPError

from vm_mgr.application import app


def get_project_token() -> str:
    """
    Get project scoped token suitable for instance creation

    :return: Admin project token
    """
    token_rq = request(
        method="POST",
        url=app.config["TOKEN_REF"],
        json=app.config["TOKEN_BODY"],
    )
    if not token_rq.ok:
        raise HTTPError(token_rq.status_code)

    return token_rq.headers["X-Subject-Token"]


def build_header():
    return {"Content-Type": "application/json", "X-Auth-Token": get_project_token()}


def get_instances() -> dict:
    """
    Make a request to get active instances from devstack.
    """
    url = f"{app.config['COMPUTE_SERVERS_REF']}/detail"
    instances_rq = request(
        method="GET",
        url=url,
        headers=build_header(),
        json=app.config["COMPUTE_LIST"],
    )

    if not instances_rq.ok:
        HTTPError(instances_rq.status_code)

    answer = {'servers': list()}
    for instance in instances_rq.json()["servers"]:
        instance_info = dict(name=instance["name"])
        instance_info["ip_addresses"] = list()
        for network, info in instance["addresses"].items():
            instance_info["ip_addresses"].extend(entry["addr"] for entry in info)
        answer['servers'].append(instance_info)

    return answer


def create_instances(flavor=None, name=None):
    """
    Function to make a request to devstack for instance creation.

    :param options: Container for additional settings for virtual machines
    """
    body = app.config["COMPUTE_CREATE"].copy()
    body["server"]["imageRef"] = get_image_ref()
    body["server"]["flavorRef"] = find_flavor_id(flavor or 'm1.nano')

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


def get_image_ref():
    """
    Get imageRef to use it in vm creation request.
    """
    images_rq = request(
        method="GET", url=app.config["IMAGE_REF"], headers=build_header(),
    )
    if not images_rq.ok:
        HTTPError(f"Can not get image id for virtual machine: {images_rq.status_code}")

    [image] = images_rq.json()["images"]
    return image["id"]


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


def find_flavor_id(flavor):
    """
    Find flavor id
    """
    for flavor in get_flavors()["flavors"]:
        if "m1.nano" == flavor["name"]:
            return flavor["id"]

    raise AttributeError(f"No flavor '{flavor}' found")
