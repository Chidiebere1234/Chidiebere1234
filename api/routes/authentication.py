# from app import jwt
from flask import request
from flask import Blueprint
from flask import jsonify, abort
from engines.models.model import User
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
    try:
        email = request.json.get('email')
        password = request.json.get('password')

        if not email or not password:
            return jsonify({'error': 'Missing email or password'}), 400

        user = User.query.filter_by(email=email).first()
        if user:
            return jsonify({'error': 'User with this email already exists'}), 400

        user = User(email=email)
        user.set_password(password)
        user.save()

        return jsonify(
            {
                'message': 'User created successfully',
                'status': 'success',
                'status_code': 201
            }
        ), 201

    except Exception as e:
        return jsonify(
            {
                'message': 'An error occurred while creating the user',    
                'error': str(e),
                'status': 'failed',
                'status_code': 500
            }
        ), 500


@auth_bp.route("/login", methods=['POST'], strict_slashes=False)
def login():
    try:
        email = request.json.get('email')
        password = request.json.get('password')

        if not email or not password:
            return jsonify({'error': 'Missing email or password'}), 400

        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            return jsonify(
                {
                    'error': 'Invalid email or password',
                    'status': 'failed',
                    'status_code': 401
                }
            ), 401

        # Create access token
        access_token = create_access_token(identity=user.id)
        return jsonify({'access_token': access_token})

    except Exception as e:
        return jsonify(
            {
                'message': 'An error occurred while creating the user',    
                'error': str(e),
                'status': 'failed',
                'status_code': 500
            }
        ), 500


# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
@auth_bp.route("/protected", methods=["GET"], strict_slashes=False)
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


@auth_bp.route("/refresh", methods=['GET'], strict_slashes=False)
@jwt_required()
def refresh():
    """ Get a new access token using user ID
    """
    current_user = get_jwt_identity()
    new_token = create_access_token(identity=current_user)
    return jsonify({'refresh_token': new_token})


@auth_bp.route("/who_am_i", methods=["GET"]) #To be renamed as profile later
@jwt_required()
def get_current_user():
    current_user = get_jwt_identity()
    user = User.query.get_or_404(id=current_user)
    return jsonify(
        id=user.id,
        email=user.email,
        username=user.username,
    )
