# app/routes/dispute.py
from flask import Blueprint, request, jsonify
from engines.models.model import Dispute
from engines.models.model import db


dispute_bp = Blueprint('dispute', __name__)

# Dispute management routes and functions
# You can place your dispute-related code here


@dispute_bp.route('/create_dispute', methods=['POST'])
def create_dispute():
	data = request.json
	new_dispute = Dispute(description=data['description'])
	db.session.add(new_dispute)
	db.session.commit()
	return jsonify({"message": "Dispute created successfully"}), 201


@dispute_bp.route('/get_disputes', methods=['GET'])
def get_disputes():
	disputes = Dispute.query.all()
	dispute_list = [dispute.serialize() for dispute in disputes]
	return jsonify(dispute_list), 200


@dispute_bp.route('/update_dispute/<int:id>', methods=['PUT'])
def update_dispute(id):
	data = request.json
	dispute = Dispute.query.get_or_404(id)
	dispute.description = data['description']
	db.session.commit()
	return jsonify({"message": "Dispute updated successfully"}), 200


@dispute_bp.route('/delete_dispute/<int:id>', methods=['DELETE'])
def delete_dispute(id):
	dispute = Dispute.query.get_or_404(id)
	db.session.delete(dispute)
	db.session.commit()
	return jsonify({"message": "Dispute deleted successfully"}), 200


@dispute_bp.route('/get_dispute/<int:id>', methods=['GET'])
def get_dispute(id):
	dispute = Dispute.query.get_or_404(id)
	return jsonify(dispute.serialize()), 200
