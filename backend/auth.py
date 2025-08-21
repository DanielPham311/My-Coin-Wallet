from flask import Blueprint, request, jsonify
from models import db, User, Wallet
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import uuid

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"error": "User already exists"}), 400
    
    user = User(username=data["username"])
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()

    # Auto-create wallet for the user
    wallet = Wallet(
        address=str(uuid.uuid4()),
        private_key=str(uuid.uuid4()),  # placeholder, later replace with crypto keypair
        user_id=user.id
    )
    db.session.add(wallet)
    db.session.commit()

    return jsonify({"message": "User registered", "wallet_address": wallet.address})

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(username=data["username"]).first()
    if user and user.check_password(data["password"]):
        token = create_access_token(identity=user.id)
        return jsonify({"access_token": token})
    return jsonify({"error": "Invalid credentials"}), 401

@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    wallets = [w.address for w in user.wallets]
    return jsonify({"username": user.username, "wallets": wallets})
