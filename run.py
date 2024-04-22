from werkzeug.middleware.proxy_fix import ProxyFix
from flask import Flask, jsonify, abort, request
from werkzeug.exceptions import HTTPException
from flask_cors import (CORS, cross_origin)
from flask_jwt_extended import JWTManager
from api.app import create_app
from os import getenv
import os


# Run App
app = create_app()

# Initialize JWT manager
jwt = JWTManager(app)

@app.route('/status', methods=['GET'], strict_slashes=False)
def status() -> str:
    """ GET /status
    Return:
      - the status of the API
    """
    return jsonify({"status": "OK"})


@app.route('/stats/', strict_slashes=False)
def stats() -> str:
    """ GET /api/v1/stats
    Return:
      - Undesided
    """
    stats = {}
    return jsonify(stats)


@app.route('/file/iwallet_ui.json', strict_slashes=False)
def file_loader():
    spec_file_path = 'iwallet_ui.json'

    try:
        # Open the JSON file and read its contents
        with open(spec_file_path, 'r') as f:
            spec_data = f.read()

        # Return the JSON data as the response
        return jsonify(json.loads(spec_data)), 200  # Assuming valid JSON format

    except FileNotFoundError:
        # Handle the case where the file is not found
        return jsonify({'error': 'Spec file not found'}), 404

    except Exception as e:
        # Handle other potential errors during file access
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

# 200 Okay
# 201 Created

@app.errorhandler(400)
def bad_request(error) -> str:
    """
    """
    return jsonify({"error": "Bad Request"}), 400


@app.errorhandler(401)
def unauthorised(error) -> str:
    """ Unautorized handler
    """
    return jsonify({"error": "Unauthorized"}), 401


# @app.errorhandler(JWTAuthorizationError)
# def unauthorized_error(e):
#   return jsonify({'error': str(e)}), 401

# @jwt.user_loader_callback_loader
# def user_loader(identity):
#   return User.query.get(identity)

# @jwt.user_lookup_loader
# def user_lookup_callback(_jwt_header, jwt_data):
#     identity = jwt_data["sub"]
#     return User.query.filter_by(id=identity).one_or_none()


@app.errorhandler(403)
def forbidden(error) -> str:
    """ Forbidden Handler
    """
    return jsonify({"error": "Forbidden"}), 403


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found Handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(500)
def server_error(error) -> str:
    """ Internal Server Error Handler
    """
    return jsonify({"error": "Internal Server Error"}), 500


# @app.before_request
# def before_any_request():
#     """ This function runs before any request is made
#         to the API Application
#     """
#     reqs = ['/auth/status/', '/auth/unauthorized/', '/auth/forbidden/']
#     if auth is None:
#         return
#     for url in reqs:
#         if auth.require_auth(request.path, url) is False:
#             return
#     if auth.authorization_header(request) is None:
#         return abort(401)
#     if auth.current_user(request) is None:
#         return abort(403)


if __name__ == '__main__':
    app.run(host='localhost', port=5005, debug=True)
