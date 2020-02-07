from uuid import uuid1
from requests import request, HTTPError

from vm_mgr.application import app


def get_project_token() -> str:
    """
    Get project scoped token suitable for instance creation.

    :return: Admin project token
    """
    body = app.config["TOKEN_BODY"].copy()
    if app.config.get("ADMIN_PROJECT_ID") is None:
        app.config["ADMIN_PROJECT_ID"] = get_admin_project_id()

    body["auth"]["scope"] = {"project": {"id": app.config["ADMIN_PROJECT_ID"]}}

    token_rq = request(method="POST", url=app.config["TOKEN_REF"], json=body,)
    if not token_rq.ok:
        raise HTTPError(token_rq.status_code)

    return token_rq.headers["X-Subject-Token"]


def get_networks() -> dict:
    """
    Fetch all networks in devstack

    :return: dictionary with networks specs
    """
    nets_rq = request(
        method="GET", url=app.config["NETWORKS_REF"], headers=build_header()
    )

    if not nets_rq:
        raise HTTPError(nets_rq.status_code)

    return nets_rq.json()


def get_network_id_by_name(name: str) -> str:
    """
    Find network id by it's name

    :return: network id in devstack
    """
    networks_info = get_networks()

    for network in networks_info["networks"]:
        if network["name"] == name:
            return network["id"]

    raise AttributeError(f"No network named {name}")


def get_admin_project_id() -> str:
    """
    Get admin project identificator

    :return: Admin project id
    """
    token_rq = request(
        method="POST", url=app.config["TOKEN_REF"], json=app.config["TOKEN_BODY"],
    )

    if not token_rq.ok:
        raise HTTPError(token_rq.status_code)

    projects_rq = request(
        method="GET",
        url=app.config["PROJECTS_REF"],
        headers=build_header(token_rq.headers["X-Subject-Token"]),
    )
    if not projects_rq.ok:
        raise HTTPError(projects_rq.status_code)

    admin_prj_id = None
    for project in projects_rq.json()["projects"]:
        if project["name"] == "admin":
            admin_prj_id = project["id"]
            break
    else:
        raise ValueError("Admin project id not found")

    return admin_prj_id


def build_header(token: str = None):
    """
    Small function to build request header
    """
    return {
        "Content-Type": "application/json",
        "X-Auth-Token": token or get_project_token(),
    }


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


def create_instances(
    flavor: str = None, name: str = None, network_name: str = None
) -> dict:
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
    body["server"]["networks"] = [
        {"uuid": get_network_id_by_name(network_name or "shared")}
    ]

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
