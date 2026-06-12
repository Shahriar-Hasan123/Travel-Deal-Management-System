from flask import jsonify


def success_response(data, status_code):
    return jsonify({"success": True, **data}), status_code


def error_response(message, status_code, error=None):
    body = {"success": False, "message": message}
    if error:
        body["error"] = error
    return jsonify(body), status_code
