from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime

from blockchain import Blockchain
from wallet import create_wallet

# -------------------- Flask Setup --------------------
app = Flask(__name__)
CORS(app)

# Secret key for JWT
app.config['SECRET_KEY'] = "super-secret-key"

# SQLite DB (swap to postgres/mysql later if needed)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blockchain.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# -------------------- Database Models --------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(200), unique=True, nullable=False)
    private_key = db.Column(db.String(200), nullable=False)

# -------------------- Blockchain Instance --------------------
blockchain = Blockchain()

# -------------------- Auth Routes --------------------
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400

    # Create wallet
    private_key, address = create_wallet()

    # Hash password
    hashed_pw = generate_password_hash(password)

    # Save user
    new_user = User(username=username, password=hashed_pw, address=address, private_key=private_key)
    db.session.add(new_user)
    db.session.commit()

    # Mint some starting balance
    blockchain.mint(address, 100)
    blockchain.create_block(previous_hash=blockchain.chain[-1]['hash'])

    return jsonify({
        "message": "User registered successfully",
        "username": username,
        "address": address,
        "private_key": private_key
    }), 201


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid credentials"}), 401

    token = jwt.encode(
        {"user_id": user.id, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
        app.config['SECRET_KEY'],
        algorithm="HS256"
    )

    return jsonify({"token": token, "address": user.address})


# -------------------- Wallet Routes --------------------
@app.route('/wallet/<address>', methods=['GET'])
def get_balance(address):
    balance = blockchain.get_balance(address)
    return jsonify({"address": address, "balance": balance})


# -------------------- Transaction Routes --------------------
@app.route('/transaction/send', methods=['POST'])
def send_transaction():
    data = request.json
    sender = data.get('sender')
    recipient = data.get('recipient')
    amount = data.get('amount')

    if not all([sender, recipient, amount]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        tx = blockchain.create_transaction(sender, recipient, amount)
        return jsonify({"message": "Transaction submitted", "transaction": tx}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/transactions/<address>', methods=['GET'])
def get_transactions(address):
    txs = blockchain.get_transactions(address)
    return jsonify({"transactions": txs})


# -------------------- Blockchain Routes --------------------
@app.route('/mine', methods=['GET'])
def mine_block():
    previous_hash = blockchain.chain[-1]['hash']
    new_block = blockchain.create_block(previous_hash)
    return jsonify({"message": "Block mined", "block": new_block})


@app.route('/chain', methods=['GET'])
def get_chain():
    return jsonify(blockchain.chain)


@app.route('/chain/validate', methods=['GET'])
def validate_chain():
    is_valid = blockchain.is_chain_valid()
    if is_valid:
        return jsonify({"message": "Blockchain is valid ✅"}), 200
    else:
        return jsonify({"message": "Blockchain is invalid ❌"}), 400


# -------------------- Run --------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()   # Creates tables on first run
    app.run(debug=True, port=5000)
