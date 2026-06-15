"""Response helpers for API routes."""

from flask import jsonify


def success_response(data, status_code=200):
    """Return a standardized success JSON response."""
    return jsonify({"success": True, **data}), status_code


def error_response(message, status_code, error=None):
    """Return a standardized error JSON response."""
    body = {"success": False, "message": message}
    if error:
        body["error"] = error
    return jsonify(body), status_code
