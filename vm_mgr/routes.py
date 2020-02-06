from flask import request

from vm_mgr.application import app
from vm_mgr.requests import get_flavors, get_instances, get_image_ref, create_instances


@app.route("/vmmgr")
def greetings():
    """
    Greetings to user
    """
    return "Hello, User! If you need help go /vmmgr/help"


@app.route("/vmmgr/servers", methods=["GET"])
def show_instances():
    """
    Get currently running instances.
    According to test task this function will return
    a list of instances in "ACTIVE" state.
    In addition instace IPv4 adresses will be added to response.
    """
    return get_instances()


@app.route("/vmmgr/servers", methods=["POST"])
def make_instances():
    """
    Create virtual machines.
    """
    body = request.json
    return create_instances(flavor=body.get('flavor'), name=body.get('name'))


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


@app.errorhandler(500)
def internal_error(error):
    """
    Internal server error handler
    """
    return f'{"code": 500, "message": "{str(error)}"}', 500


@app.errorhandler(403)
def forbidden(error):
    """
    Forbidden error handler
    """
    return f'{"code": 403, "message": "Not found"}', 403


@app.errorhandler(404)
def not_found(error):
    """
    This function handles a situation when requested route is
    absent.
    """
    return f'{"code": 404, "message": "Not found"}', 404
