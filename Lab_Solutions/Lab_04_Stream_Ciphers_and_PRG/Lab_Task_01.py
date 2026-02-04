"""
salsa_stream_cipher.py

Designed stream cipher (Salsa20-based) with a per-message KDF.

- master_key: 32-byte long-term secret (shared between sender and receiver)
- msg_nonce: 8-byte public, per-message nonce (if not provided, it is randomly generated)
- Derivation: HMAC-SHA256(master_key, msg_nonce || info) -> PRK
  Expand PRK with HMAC to get subkey (32 bytes) and derived_nonce (8 bytes for Salsa20).
- Encryption/Decryption: Salsa20 keystream XOR (via PyCryptodome API).

Note: This implementation demonstrates confidentiality only (no authentication/MAC).
      For real systems, use authenticated encryption (AEAD) or add an HMAC.
"""

from Crypto.Cipher import Salsa20
from Crypto.Hash import HMAC, SHA256
from Crypto.Random import get_random_bytes
from typing import Tuple, Dict

# -------------------------
# KDF (small HKDF-like)
# -------------------------
def _hkdf_like(master_key: bytes, msg_nonce: bytes, info: bytes = b'') -> Tuple[bytes, bytes]:
    """
    Derive (subkey, derived_nonce) deterministically from master_key and msg_nonce.
    - master_key: 32 bytes
    - msg_nonce: arbitrary bytes (we use 8 bytes externally)
    Returns:
    - subkey (32 bytes) : Salsa20 key
    - derived_nonce (8 bytes) : Salsa20 nonce
    """
    if len(master_key) < 16:
        raise ValueError("master_key should be at least 16 bytes; 32 bytes recommended")

    # Extract step: PRK = HMAC(master_key, msg_nonce || info)
    h = HMAC.new(master_key, digestmod=SHA256)
    h.update(msg_nonce)
    h.update(info)
    prk = h.digest()  # 32 bytes

    # Expand helper: HMAC(prk, counter || label) and take needed bytes
    def expand(label: bytes, out_len: int, counter: int = 1) -> bytes:
        ctr = bytes([counter])
        hm = HMAC.new(prk, digestmod=SHA256)
        hm.update(ctr + label)
        return hm.digest()[:out_len]

    subkey = expand(b"salt-subkey", 32, counter=1)
    derived_nonce = expand(b"salt-nonce", 8, counter=2)
    return subkey, derived_nonce

# -------------------------
# Encryption / Decryption
# -------------------------
def encrypt(master_key: bytes, plaintext: bytes, msg_nonce: bytes = None, info: bytes = b'') -> Dict:
    """
    Encrypt plaintext using Salsa20 with a per-message derived key/nonce.

    Returns a dict with:
      - ciphertext: bytes
      - msg_nonce: bytes (8 bytes) public nonce used (caller-supplied or generated)
      - info: bytes (optional context information) -- echoed back
    """
    if len(master_key) < 16:
        raise ValueError("master_key must be at least 16 bytes (32 recommended)")

    if msg_nonce is None:
        msg_nonce = get_random_bytes(8)  # public per-message nonce

    subkey, derived_nonce = _hkdf_like(master_key, msg_nonce, info)
    cipher = Salsa20.new(key=subkey, nonce=derived_nonce)  # Salsa20 expects 8-byte nonce
    ciphertext = cipher.encrypt(plaintext)

    return {
        "ciphertext": ciphertext,
        "msg_nonce": msg_nonce,
        "info": info
    }

def decrypt(master_key: bytes, ciphertext: bytes, msg_nonce: bytes, info: bytes = b'') -> bytes:
    """
    Decrypt ciphertext using the same master_key and msg_nonce used for encryption.
    Returns plaintext bytes.
    """
    subkey, derived_nonce = _hkdf_like(master_key, msg_nonce, info)
    cipher = Salsa20.new(key=subkey, nonce=derived_nonce)
    return cipher.decrypt(ciphertext)

# -------------------------
# Example / quick test
# -------------------------
if __name__ == "__main__":
    # generate a master key (in practice this is shared securely)
    master_key = get_random_bytes(32)

    message = b"Confidential lab message: do not reveal."
    print("Original:", message)

    # Encrypt (auto nonce)
    out = encrypt(master_key, message)
    ct = out["ciphertext"]
    nonce = out["msg_nonce"]
    print("Ciphertext (hex):", ct.hex())
    print("msg_nonce (hex):", nonce.hex())

    # Decrypt
    recovered = decrypt(master_key, ct, nonce)
    print("Recovered:", recovered)
    assert recovered == message, "decryption failed!"

    # Example: caller-supplied nonce (must be same at decrypt)
    custom_nonce = b"\x00\x01\x02\x03\x04\x05\x06\x07"
    out2 = encrypt(master_key, b"Another message", msg_nonce=custom_nonce)
    r2 = decrypt(master_key, out2["ciphertext"], custom_nonce)
    print("Recovered 2:", r2)
