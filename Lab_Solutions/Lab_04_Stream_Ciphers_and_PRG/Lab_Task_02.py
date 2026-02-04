"""
salsa_attacks.py

Demonstrates adversarial attacks on a Salsa20-based stream cipher
which uses a simple HMAC-SHA256-based KDF to produce per-message
subkey and derived_nonce from a long-term master_key and a public msg_nonce.

Attacks:
 - nonce_reuse_known_plaintext: recover plaintext2 when nonce is reused and plaintext1 known
 - bit_flip_malleability: modify ciphertext to flip bits in plaintext

Run: python salsa_attacks.py
Requires: pip install pycryptodome
"""

from Crypto.Cipher import Salsa20
from Crypto.Hash import HMAC, SHA256
from Crypto.Random import get_random_bytes
import binascii

# ---------------------------
# Re-implement small KDF & encrypt/decrypt so this file is standalone
# ---------------------------
def _hkdf_like(master_key: bytes, msg_nonce: bytes, info: bytes = b''):
    h = HMAC.new(master_key, digestmod=SHA256)
    h.update(msg_nonce)
    h.update(info)
    prk = h.digest()
    def expand(label: bytes, out_len: int, counter: int = 1):
        ctr = bytes([counter])
        hm = HMAC.new(prk, digestmod=SHA256)
        hm.update(ctr + label)
        return hm.digest()[:out_len]
    subkey = expand(b"salt-subkey", 32, counter=1)
    derived_nonce = expand(b"salt-nonce", 8, counter=2)
    return subkey, derived_nonce

def encrypt(master_key: bytes, plaintext: bytes, msg_nonce: bytes = None, info: bytes = b''):
    if msg_nonce is None:
        msg_nonce = get_random_bytes(8)
    subkey, derived_nonce = _hkdf_like(master_key, msg_nonce, info)
    cipher = Salsa20.new(key=subkey, nonce=derived_nonce)
    ciphertext = cipher.encrypt(plaintext)
    return {"ciphertext": ciphertext, "msg_nonce": msg_nonce}

def decrypt(master_key: bytes, ciphertext: bytes, msg_nonce: bytes, info: bytes = b''):
    subkey, derived_nonce = _hkdf_like(master_key, msg_nonce, info)
    cipher = Salsa20.new(key=subkey, nonce=derived_nonce)
    return cipher.decrypt(ciphertext)

# ---------------------------
# ATTACK FUNCTIONS
# ---------------------------
def attack_nonce_reuse_known_plaintext(cipher1: bytes, cipher2: bytes, known_plain1: bytes) -> bytes:
    """
    Given ciphertexts cipher1, cipher2 that share the same keystream (nonce reuse),
    and known plaintext for the first message, recover plaintext2 where lengths overlap.
    """
    # compute keystream from cipher1 and known_plain1 (up to overlap)
    L = min(len(cipher1), len(known_plain1))
    keystream_part = bytes([c ^ p for c, p in zip(cipher1[:L], known_plain1[:L])])
    # recover corresponding part of plaintext2
    recovered_part = bytes([c ^ k for c, k in zip(cipher2[:L], keystream_part)])
    # if cipher2 longer than known overlap, append placeholder bytes for unrecovered tail
    if len(cipher2) > L:
        recovered_part += b"?" * (len(cipher2) - L)
    return recovered_part

def attack_two_ciphertexts_xor(cipher1: bytes, cipher2: bytes) -> bytes:
    """
    If two ciphertexts share the same keystream, XORing them yields plaintext1 XOR plaintext2.
    This can leak structure, patterns, or be used with crib-dragging.
    """
    L = min(len(cipher1), len(cipher2))
    return bytes([a ^ b for a, b in zip(cipher1[:L], cipher2[:L])])

def attack_bit_flip(ciphertext: bytes, flip_map: dict) -> bytes:
    """
    flip_map: {index: xor_byte} indicating which bytes to XOR in the ciphertext
    Returns modified ciphertext
    """
    c = bytearray(ciphertext)
    for idx, xor_byte in flip_map.items():
        if 0 <= idx < len(c):
            c[idx] ^= xor_byte
    return bytes(c)

# ---------------------------
# DEMONSTRATION
# ---------------------------
def demo():
    print("=== Salsa20-based stream cipher attacks demo ===")
    master_key = get_random_bytes(32)
    print("master_key (hex):", binascii.hexlify(master_key).decode())

    # Two plaintexts
    pt1 = b"Hello Alice, the launch is at 0400 hours."
    pt2 = b"Meet at rendezvous point: Warehouse 12."

    # BAD: reuse same msg_nonce for both messages (attacker can observe ciphertexts)
    reused_nonce = get_random_bytes(8)
    out1 = encrypt(master_key, pt1, msg_nonce=reused_nonce)
    out2 = encrypt(master_key, pt2, msg_nonce=reused_nonce)
    c1 = out1["ciphertext"]
    c2 = out2["ciphertext"]

    print("\nCiphertext1 (hex):", c1.hex())
    print("Ciphertext2 (hex):", c2.hex())

    # Attack 1: attacker knows plaintext1 (e.g., it's a header or predictable string)
    print("\n--- Attack 1: Nonce-reuse + known-plaintext ---")
    known_plain1 = pt1  # attacker knows pt1 entirely (worst-case)
    recovered_pt2 = attack_nonce_reuse_known_plaintext(c1, c2, known_plain1)
    print("Recovered pt2 (partial or full):", recovered_pt2)
    print("Original pt2 :                ", pt2)

    # Attack 1b: attacker does not fully know pt1 but can XOR ciphertexts to get pt1^pt2
    print("\n--- Attack 1b: ciphertext1 XOR ciphertext2 => pt1 XOR pt2 ---")
    pxor = attack_two_ciphertexts_xor(c1, c2)
    print("pt1 ^ pt2 (hex):", pxor.hex())
    # show we can XOR known pt1 to get pt2 if some bits of pt1 are known:
    # e.g., attacker guesses a small crib "Meet" at start of pt2, can attempt crib-dragging (not implemented here)

    # Attack 2: Bit-flip malleability
    print("\n--- Attack 2: Bit-flip (malleability) ---")
    # Suppose attacker wants to change "0400" -> "0500" in pt1
    # find index of '0' in plaintext (first occurrence)
    idx = pt1.find(b"0400")
    if idx != -1:
        # We'll flip the character '4' -> '5' (0x34 -> 0x35): delta = 0x01
        # position of '4' is idx+1
        target_pos = idx + 1
        delta = 0x34 ^ 0x35  # 1
        modified_c1 = attack_bit_flip(c1, {target_pos: delta})
        modified_pt1 = decrypt(master_key, modified_c1, reused_nonce)
        print("Original pt1 :", pt1)
        print("Modified pt1 :", modified_pt1)
        print("Change observed at pos", target_pos, ":", modified_pt1[target_pos-5:target_pos+5])
    else:
        print("Couldn't find pattern '0400' to demo targeted flip. Showing generic flip instead:")
        modified_c1 = attack_bit_flip(c1, {0: 0xFF})
        print("Decrypted modified:", decrypt(master_key, modified_c1, reused_nonce))

    # Note: in correct usage (unique nonces), these attacks are mitigated.
    # Show proper usage: distinct nonces
    print("\n--- Proper usage: distinct nonces prevents keystream reuse ---")
    outA = encrypt(master_key, pt1)   # random nonce
    outB = encrypt(master_key, pt2)   # random nonce
    # XOR of ciphertexts no longer equates to plaintext XOR since keystreams differ
    xor_distinct = attack_two_ciphertexts_xor(outA["ciphertext"], outB["ciphertext"])
    print("ciphertextA XOR ciphertextB (hex):", xor_distinct.hex()[:80], "... (differs from pt1^pt2)")

if __name__ == "__main__":
    demo()
