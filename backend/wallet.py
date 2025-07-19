from ecdsa import SigningKey, SECP256k1
import hashlib

def create_wallet():
    private_key = SigningKey.generate(curve=SECP256k1)
    public_key = private_key.get_verifying_key()
    address = hashlib.sha256(public_key.to_string()).hexdigest()
    return private_key.to_string().hex(), address
