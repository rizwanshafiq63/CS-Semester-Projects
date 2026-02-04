import random

# Basic Functions: mod_exp, extended GCD, mod_inverse
def mod_exp(base, exponent, modulus):
    result = 1
    base %= modulus
    while exponent > 0:
        if exponent % 2 == 1:          
            result = (result * base) % modulus
        base = (base * base) % modulus  
        exponent //= 2                  
    return result

def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return g, x, y

def mod_inverse(a, p):
    a %= p
    g, x, y = extended_gcd(a, p)
    if g != 1:
        raise ValueError(f"No modular inverse exists for {a} mod {p}")
    return x % p

# ElGamal over integers (same as Question 3 style)
def elgamal_keygen(p, g):
    x = random.randint(2, p - 2)      # private key
    h = mod_exp(g, x, p)              # h = g^x mod p
    return (p, g, h), x

def elgamal_encrypt(m, p, g, h):
    if not (0 <= m < p):
        raise ValueError("Message m must satisfy 0 <= m < p")
    k = random.randint(2, p - 2) 
    c1 = mod_exp(g, k, p)
    s  = mod_exp(h, k, p)
    c2 = (m * s) % p
    return c1, c2

def elgamal_decrypt(c1, c2, x, p):
    s = mod_exp(c1, x, p)
    s_inv = mod_inverse(s, p)
    m = (c2 * s_inv) % p
    return m

# Diffie–Hellman: To compute shared key
def diffie_hellman_shared_key(p, g, a, b):
    A = mod_exp(g, a, p)      # Alice's public
    B = mod_exp(g, b, p)      # Bob's public
    # Shared keys
    K_A = mod_exp(B, a, p)
    K_B = mod_exp(A, b, p)
    assert K_A == K_B
    return K_A, A, B

# Helper: use K_DH as XOR key for a byte string
def int_to_key_bytes(k):
    if k == 0:
        return [0]
    bytes_list = []
    while k > 0:
        bytes_list.append(k % 256)
        k //= 256
    bytes_list.reverse()
    return bytes_list

def xor_with_key_bytes(data_bytes, key_bytes):
    result = []
    key_len = len(key_bytes)
    for i, b in enumerate(data_bytes):
        kb = key_bytes[i % key_len]
        result.append(b ^ kb)
    return result

def hybrid_encrypt(message, p, g, dh_key, elgamal_public):
    p_e, g_e, h_e = elgamal_public

    # 1. Convert message to bytes (ASCII)
    msg_bytes = [ord(ch) for ch in message]

    # 2. Derive key bytes from dh_key
    key_bytes = int_to_key_bytes(dh_key)

    # 3. XOR-mask message bytes
    masked_bytes = xor_with_key_bytes(msg_bytes, key_bytes)

    # 4. Encrypt each masked byte using ElGamal
    ciphertexts = []
    for mb in masked_bytes:
        c1, c2 = elgamal_encrypt(mb, p_e, g_e, h_e)
        ciphertexts.append((c1, c2))

    return ciphertexts

def hybrid_decrypt(ciphertexts, p, g, dh_key, elgamal_private):
    # 1. Decrypt to get masked bytes
    masked_bytes = []
    for (c1, c2) in ciphertexts:
        mb = elgamal_decrypt(c1, c2, elgamal_private, p)
        masked_bytes.append(mb)

    # 2. XOR-unmask using dh_key
    key_bytes = int_to_key_bytes(dh_key)
    recovered_bytes = xor_with_key_bytes(masked_bytes, key_bytes)

    # 3. Convert bytes back to string
    chars = [chr(b) for b in recovered_bytes]
    return "".join(chars)

if __name__ == "__main__":
    p = 31847
    g = 5
    print("=== Hybrid DH + ElGamal Encryption (Question 5) ===")
    # Step 1: Diffie–Hellman key exchange
    a = random.randint(2, p - 2)   # Alice's private
    b = random.randint(2, p - 2)   # Bob's private

    K_DH, A, B = diffie_hellman_shared_key(p, g, a, b)

    print(f"DH parameters: p = {p}, g = {g}")
    print(f"Alice's private a : {a}")
    print(f"Bob's private b   : {b}")
    print(f"Alice's public A  : {A}")
    print(f"Bob's public B    : {B}")
    print(f"Shared DH key K_DH: {K_DH}")
    print()

    # Step 2: ElGamal key generation
    elgamal_public, elgamal_private = elgamal_keygen(p, g)
    p_e, g_e, h_e = elgamal_public

    print("ElGamal public key (p, g, h):", elgamal_public)
    print("ElGamal private key x       :", elgamal_private)
    print()

    # Step 3: Hybrid encryption of test message
    message = "HYBRID CRYPTO SYSTEM"
    print("Original message:", message)

    ciphertexts = hybrid_encrypt(message, p, g, K_DH, elgamal_public)

    print("\nCiphertexts (per character):")
    for i, (c1, c2) in enumerate(ciphertexts):
        print(f"  char[{i}] -> (c1={c1}, c2={c2})")
        
    # Step 4: Hybrid decryption
    decrypted_message = hybrid_decrypt(ciphertexts, p, g, K_DH, elgamal_private)
    print("\nDecrypted message:", decrypted_message)

    print("\nDecryption successful:", decrypted_message == message)
