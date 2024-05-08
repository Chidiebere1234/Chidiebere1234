from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask import Blueprint, request, jsonify
from engines.models.model import Dispute
from engines.models.model import db


dispute_bp = Blueprint('dispute', __name__)


@dispute_bp.route('/create_dispute', methods=['POST'], strict_slashes=False)
@jwt_required()
def create_dispute():
	data = request.json
	user_id = get_jwt_identity()
	new_dispute = Dispute(
		user_id=user_id,
		title=data['title'],
		category=data['category'],
		description=data['description']
	)

	new_dispute.save()
	return jsonify({"message": "Dispute created successfully"}), 201


@dispute_bp.route('/get_all_disputes', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_disputes():
	disputes = Dispute.query.all()
	dispute_list = [dispute.serialize() for dispute in disputes]
	return jsonify(dispute_list), 200


@dispute_bp.route('/get_dispute/<int:id>', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_dispute(id):
	dispute = Dispute.query.get_or_404(id)
	return jsonify(dispute.serialize()), 200


@dispute_bp.route('/update_dispute/<int:id>', methods=['PUT'], strict_slashes=False)
@jwt_required()
def update_dispute(id):
	data = request.json
	dispute = Dispute.query.get_or_404(id)
	dispute.description = data['description']
	db.session.commit()
	return jsonify({"message": "Dispute updated successfully"}), 200


@dispute_bp.route('/delete_dispute/<int:id>', methods=['DELETE'], strict_slashes=False)
@jwt_required()
def delete_dispute(id):
	dispute = Dispute.query.get_or_404(id)
	dispute._delete()

	return jsonify({"message": "Dispute deleted successfully"}), 200
