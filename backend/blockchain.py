import hashlib
import json
from time import time

class Blockchain:
    def __init__(self):
        self.chain = []
        self.mempool = []
        self.create_block(previous_hash='0')  # Genesis block

    def create_block(self, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.mempool,
            'previous_hash': previous_hash,
            'nonce': 0
        }
        block['hash'] = self.hash(block)
        self.mempool = []
        self.chain.append(block)
        return block

    def add_transaction(self, sender, receiver, amount):
        self.mempool.append({'sender': sender, 'receiver': receiver, 'amount': amount})
        return len(self.chain) + 1

    def proof_of_work(self, block):
        while not block['hash'].startswith('0000'):
            block['nonce'] += 1
            block['hash'] = self.hash(block)
        return block

    @staticmethod
    def hash(block):
        block_copy = block.copy()
        block_copy.pop('hash', None)
        encoded = json.dumps(block_copy, sort_keys=True).encode()
        return hashlib.sha256(encoded).hexdigest()

    def get_balance(self, address):
        balance = 0
        for block in self.chain:
            for tx in block['transactions']:
                if tx['sender'] == address:
                    balance -= tx['amount']
                if tx['receiver'] == address:
                    balance += tx['amount']
        return balance
