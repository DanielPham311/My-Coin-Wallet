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
    return jsonify({"private_key": private_key, "address": address})

@app.route('/wallet/<address>', methods=['GET'])
def get_balance(address):
    balance = blockchain.get_balance(address)
    return jsonify({"address": address, "balance": balance})

@app.route('/transaction', methods=['POST'])
def create_transaction():
    data = request.json
    blockchain.add_transaction(data['sender'], data['receiver'], data['amount'])
    return jsonify({"message": "Transaction added"})

@app.route('/mine', methods=['GET'])
def mine_block():
    last_block = blockchain.chain[-1]
    new_block = {'index': len(blockchain.chain) + 1,
                 'timestamp': last_block['timestamp'],
                 'transactions': blockchain.mempool,
                 'previous_hash': last_block['hash'],
                 'nonce': 0}
    mined_block = blockchain.proof_of_work(new_block)
    blockchain.chain.append(mined_block)
    return jsonify({"message": "Block mined", "block": mined_block})

@app.route('/chain', methods=['GET'])
def get_chain():
    return jsonify(blockchain.chain)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
