# from app import jwt
from flask import request
from flask import Blueprint
from flask import jsonify, abort
from engine.models.model import User
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required


auth_bp = Blueprint('authentication', __name__)


@auth_bp.route('/unauthorized', strict_slashes=False)
def unauth() -> str:
    """ GET /api/auth/unauthorized
    Return:
        - if user is not authorized
    """
    return abort(401)


@auth_bp.route('/forbidden', strict_slashes=False)
def forbid() -> str:
    """ GET /api/auth/forbidden
    Return:
        - if forbidden
    """
    return abort(403)


@auth_bp.route('/bad-request', strict_slashes=False)
def bad_request() -> str:
	""" GET /api/auth/bad-request
	Return:
		- If an unknown request and submitted
	"""
	return abort(400)


@auth_bp.route("/signup", methods=['POST'], strict_slashes=False)
def signup():
    username = request.json.get('username')
    password = request.json.get('password')

    if not username or not password:
        return jsonify({'error': 'Missing username or password'}), 400

    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify({'error': 'Username already exists'}), 400

    user = User(username=username)
    user.set_password(password)
    user.save()

    return jsonify({'message': 'User created successfully'}), 201


@auth_bp.route("/login", methods=['POST'], strict_slashes=False)
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    if not username or not password:
        return jsonify({'error': 'Missing username or password'}), 400

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password): #check_password_hash(user.password_hash, password):
        return jsonify({'error': 'Invalid username or password'}), 401

    # Create access token
    access_token = create_access_token(identity=user.id)
    return jsonify({'access_token': access_token})


# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
@auth_bp.route("/protected", methods=["GET"], strict_slashes=False)
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


@auth_bp.route("/refresh", methods=['POST'], strict_slashes=False)
@jwt_required()
def refresh():
    current_user = get_jwt_identity()  # Get user ID from access token
    new_token = create_access_token(identity=current_user)
    return jsonify({'refresh_token': new_token})


@auth_bp.route("/who_am_i", methods=["GET"])
@jwt_required()
def get_current_user():
    return jsonify(
        id=current_user.id,
        email=current_user.email,
        username=current_user.username,
    )