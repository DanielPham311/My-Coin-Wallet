from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from blockchain import Blockchain
import datetime

app = Flask(__name__)

# Config
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["JWT_SECRET_KEY"] = "super-secret"  # change this in production
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

blockchain = Blockchain()

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# =====================
# Auth Endpoints
# =====================
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    hashed_pw = bcrypt.generate_password_hash(data["password"]).decode("utf-8")
    new_user = User(username=data["username"], password=hashed_pw)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully!"}), 201

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data["username"]).first()
    if user and bcrypt.check_password_hash(user.password, data["password"]):
        token = create_access_token(identity=user.username, expires_delta=datetime.timedelta(hours=1))
        return jsonify({"token": token, "username": user.username}), 200
    return jsonify({"message": "Invalid credentials"}), 401

# =====================
# Blockchain Endpoints
# =====================
@app.route("/balance", methods=["GET"])
@jwt_required()
def get_balance():
    current_user = get_jwt_identity()
    balance = blockchain.get_balance(current_user)
    return jsonify({"balance": balance}), 200

@app.route("/transactions", methods=["GET"])
@jwt_required()
def get_transactions():
    current_user = get_jwt_identity()
    txs = blockchain.get_user_transactions(current_user)
    return jsonify({"transactions": txs}), 200

@app.route("/transaction/send", methods=["POST"])
@jwt_required()
def send_transaction():
    current_user = get_jwt_identity()
    data = request.get_json()
    receiver = data.get("receiver")
    amount = data.get("amount")

    if not receiver or not amount:
        return jsonify({"message": "Missing receiver or amount"}), 400

    tx = blockchain.add_transaction(sender=current_user, receiver=receiver, amount=amount)
    return jsonify({"message": "Transaction added", "transaction": tx}), 201

@app.route("/mint", methods=["POST"])
@jwt_required()
def mint():
    current_user = get_jwt_identity()
    data = request.get_json()
    amount = data.get("amount")

    if not amount:
        return jsonify({"message": "Missing amount"}), 400

    tx = blockchain.add_transaction(sender="SYSTEM", receiver=current_user, amount=amount)
    return jsonify({"message": f"{amount} coins minted", "transaction": tx}), 201

# =====================
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
