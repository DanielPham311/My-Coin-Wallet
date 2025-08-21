import hashlib
import json
from time import time
from db import get_db_connection


class Blockchain:
    def __init__(self):
        self.chain = []
        self.mempool = []
        self.create_block(previous_hash='0')  # Genesis block

    def create_block(self, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.mempool.copy(),
            'previous_hash': previous_hash,
            'nonce': 0
        }
        block = self.proof_of_work(block)
        block['hash'] = self.hash(block)
        self.chain.append(block)

        # Persist mined transactions into DB
        conn = get_db_connection()
        cur = conn.cursor()
        for tx in block['transactions']:
            cur.execute(
                """
                INSERT INTO transactions (sender, recipient, amount, timestamp, block_index)
                VALUES (%s, %s, %s, NOW(), %s)
                """,
                (tx['sender'], tx['receiver'], tx['amount'], block['index'])
            )

            # Update balances in DB
            if tx['sender'] != "SYSTEM":  # Skip system mint
                cur.execute(
                    "UPDATE users SET balance = balance - %s WHERE address = %s",
                    (tx['amount'], tx['sender'])
                )
            cur.execute(
                "UPDATE users SET balance = balance + %s WHERE address = %s",
                (tx['amount'], tx['receiver'])
            )
        conn.commit()
        cur.close()
        conn.close()

        self.mempool = []
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
        if self.get_balance(sender) < amount:
            raise Exception("Insufficient balance")

        transaction = {
            "sender": sender,
            "receiver": recipient,
            "amount": amount
        }

        self.add_transaction(sender, recipient, amount)

        # Mine transaction immediately
        block = self.create_block(previous_hash=self.chain[-1]['hash'])
        return transaction

    def sign_transaction(self, sender, receiver, amount, private_key):
        payload = f"{sender}{receiver}{amount}{private_key}"
        return hashlib.sha256(payload.encode()).hexdigest()

    def mint(self, receiver, amount):
        """System-generated coins"""
        self.mempool.append({
            'sender': 'SYSTEM',
            'receiver': receiver,
            'amount': amount
        })

    def is_chain_valid(self, chain=None):
        if chain is None:
            chain = self.chain
        for i in range(1, len(chain)):
            current_block = chain[i]
            prev_block = chain[i - 1]

            if current_block['hash'] != self.hash(current_block):
                return False
            if current_block['previous_hash'] != prev_block['hash']:
                return False
            if not current_block['hash'].startswith('0000'):
                return False
        return True

    @staticmethod
    def hash(block):
        block_copy = block.copy()
        block_copy.pop('hash', None)
        encoded = json.dumps(block_copy, sort_keys=True).encode()
        return hashlib.sha256(encoded).hexdigest()

    def get_balance(self, address):
        """Get balance from DB (single source of truth)"""
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT balance FROM users WHERE address = %s", (address,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        return row[0] if row else 0

    def get_transactions(self, address):
        """Fetch transactions from DB instead of scanning chain"""
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT sender, recipient, amount, timestamp, block_index
            FROM transactions
            WHERE sender = %s OR recipient = %s
            ORDER BY timestamp DESC
            """,
            (address, address)
        )
        rows = cur.fetchall()
        cur.close()
        conn.close()

        transactions = []
        for row in rows:
            transactions.append({
                "sender": row[0],
                "receiver": row[1],
                "amount": row[2],
                "timestamp": row[3].isoformat(),
                "block_index": row[4]
            })
        return transactions
