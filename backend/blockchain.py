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
            'transactions': self.mempool.copy(),  # important: copy current mempool
            'previous_hash': previous_hash,
            'nonce': 0
        }
        block = self.proof_of_work(block)
        block['hash'] = self.hash(block)
        self.chain.append(block)
        self.mempool = []  # clear mempool only after adding block
        return block

    def proof_of_work(self, block):
        block['nonce'] = 0
        computed_hash = self.hash(block)
        while not computed_hash.startswith('0000'):
            block['nonce'] += 1
            computed_hash = self.hash(block)
        block['hash'] = computed_hash
        return block

    def add_transaction(self, sender, receiver, amount):
        self.mempool.append({
            'sender': sender,
            'receiver': receiver,
            'amount': amount
        })
        return len(self.chain) + 1

    def create_transaction(self, sender, recipient, amount):
        # Validate keys, balances, and sign if needed
        if self.get_balance(sender) < amount:
            raise Exception("Insufficient balance")

        transaction = {
            "sender": sender,
            "recipient": recipient,
            "amount": amount
        }

        # Add to mempool
        self.add_transaction(sender, recipient, amount)

        # Mine transaction immediately
        block = self.create_block(previous_hash=self.chain[-1]['hash'])
        self.proof_of_work(block)

        return transaction


    def sign_transaction(self, sender, receiver, amount, private_key):
        payload = f"{sender}{receiver}{amount}{private_key}"
        return hashlib.sha256(payload.encode()).hexdigest()

    def mint(self, receiver, amount):
        self.mempool.append({
            'sender': 'SYSTEM',
            'receiver': receiver,
            'amount': amount
        })

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

    def get_transaction_history(self, address):
        history = []
        for block in self.chain:
            for tx in block['transactions']:
                if tx['sender'] == address or tx['receiver'] == address:
                    history.append(tx)
        return history
