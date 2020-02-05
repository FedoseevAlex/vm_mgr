from flask import request

from vm_mgr.application import app
from vm_mgr.requests import get_flavors, get_instances, get_image_ref


@app.route("/vmmgr")
def greetings():
    """
    Greetings to user
    """
    return "Hello, User! If you need help go /vmmgr/help"


@app.route("/vmmgr/help")
@app.route("/vmmgr/usage")
def get_help():
    """
    Prints some simple usage info
    """


@app.route("/vmmgr/servers", methods=["GET"])
def show_instances():
    """
    Get currently runnining instances.
    According to test task this function will return
    a list of instances in "ACTIVE" state.
    In addition instace IPv4 adresses will be added to response.
    """
    return get_instances()


@app.route("/vmmgr/servers", methods=["POST"])
def create_instances():
    """
    Create virtual machines.
    """

@app.route("/vmmgr/flavors", methods=["GET"])
def show_flavors():
    """
    Show all available flavors
    """
    return get_flavors()

@app.route("/vmmgr/images", methods=["GET"])
def show_image_ref():
    """
    Show all available images
    """
    return get_image_ref()

@app.errorhandler(404)
def not_found(error):
    """
    This function handles a situation when requested route is
    absent.
    """
    return f'{"Error code": 404, "error": "{str(error)}"}', 404
