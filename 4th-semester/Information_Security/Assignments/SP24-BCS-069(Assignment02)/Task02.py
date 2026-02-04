# Task02 — Q2. DES Double Encryption (DES(K1) then DES(K2))

from Crypto.Cipher import DES
from Crypto.Random import get_random_bytes
import base64

# --- PKCS7 padding for 8-byte DES blocks ---
def pkcs7_pad(data: bytes, block_size: int = 8) -> bytes:
    pad_len = block_size - (len(data) % block_size)
    return data + bytes([pad_len]) * pad_len

def pkcs7_unpad(padded: bytes, block_size: int = 8) -> bytes:
    if not padded or len(padded) % block_size != 0:
        raise ValueError("Invalid padded data length")
    pad_len = padded[-1]
    if pad_len < 1 or pad_len > block_size or padded[-pad_len:] != bytes([pad_len]) * pad_len:
        raise ValueError("Invalid PKCS7 padding")
    return padded[:-pad_len]


def double_des_encrypt(k1: bytes, k2: bytes, data: bytes) -> bytes:
    # E_k2( E_k1(m) )
    cipher = DES.new(k1, DES.MODE_ECB)
    c1 = cipher.encrypt(pkcs7_pad(data, 8)) # produces padded ciphertext 
    cipher2 = DES.new(k2, DES.MODE_ECB)
    c2 = cipher2.encrypt(c1)
    return c2

def double_des_decrypt(k1: bytes, k2: bytes, data: bytes) -> bytes:
    # D_k1( D_k2(c) )
    cipher2 = DES.new(k2, DES.MODE_ECB)
    step = cipher2.decrypt(data)
    cipher = DES.new(k1, DES.MODE_ECB)
    plain = pkcs7_unpad(cipher.decrypt(step), 8)
    return plain

def main():
    msg = input("Enter plaintext: ").encode('utf-8')
    # Random keys
    k1 = get_random_bytes(8)
    k2 = get_random_bytes(8)
    print(f"K1 (hex): {k1.hex()}")
    print(f"K2 (hex): {k2.hex()}")

    ct_double = double_des_encrypt(k1, k2, msg)
    print(f"Double-DES ciphertext (base64): {base64.b64encode(ct_double).decode()}")
    recovered = double_des_decrypt(k1, k2, ct_double).decode('utf-8')
    print("Recovered plaintext:", recovered)

    # Test with K1 = K2
    print("\n=== Test when K1 = K2 ===")
    k = get_random_bytes(8)
    single_cipher = DES.new(k, DES.MODE_ECB)
    ct_single = single_cipher.encrypt(pkcs7_pad(msg, 8))

    ct_double_same = double_des_encrypt(k, k, msg)
    print("Single DES ct (hex):", ct_single.hex())
    print("Double DES with K1=K2 ct (hex):", ct_double_same.hex())
    print("Behaves like Single DES? ->", ct_single == ct_double_same)

if __name__ == "__main__":
    main()