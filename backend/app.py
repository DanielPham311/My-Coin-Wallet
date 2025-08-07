from flask import Flask, request, jsonify
from flask_cors import CORS
from blockchain import Blockchain
from wallet import create_wallet

app = Flask(__name__)
CORS(app)

blockchain = Blockchain()

@app.route('/wallet/create', methods=['POST'])
def wallet_create():
    private_key, address = create_wallet()

    # Mint 100 coins
    blockchain.mint(address, 100)

    # Confirm minting by mining the block
    blockchain.create_block(previous_hash=blockchain.chain[-1]['hash'])

    balance = blockchain.get_balance(address)
    return jsonify({
        "private_key": private_key,
        "address": address,
        "balance": balance
    })


@app.route('/wallet/<address>', methods=['GET'])
def get_balance(address):
    balance = blockchain.get_balance(address)
    return jsonify({"address": address, "balance": balance})


@app.route('/transaction/send', methods=['POST'])
def send_transaction():
    data = request.json
    sender = data.get('sender')
    recipient = data.get('recipient')
    amount = data.get('amount')
    private_key = data.get('privateKey')

    if not all([sender, recipient, amount, private_key]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        tx = blockchain.create_transaction(sender, recipient, amount)
        return jsonify({"message": "Transaction submitted", "transaction": tx}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/mine', methods=['GET'])
def mine_block():
    previous_hash = blockchain.chain[-1]['hash']
    new_block = blockchain.create_block(previous_hash)
    return jsonify({"message": "Block mined", "block": new_block})


@app.route('/chain', methods=['GET'])
def get_chain():
    return jsonify(blockchain.chain)


@app.route('/transactions/<address>', methods=['GET'])
def get_transactions(address):
    history = blockchain.get_transaction_history(address)
    return jsonify({"address": address, "transactions": history})


if __name__ == '__main__':
    app.run(debug=True, port=5000)
