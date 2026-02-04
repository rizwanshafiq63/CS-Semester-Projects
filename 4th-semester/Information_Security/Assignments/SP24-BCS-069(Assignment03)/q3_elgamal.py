import random

# Extended Euclidean Algorithm for modular inverse
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
        raise ValueError("No inverse exists!")
    return x % p

# ElGamal Key Generation
def mod_exp(base, exponent, modulus): # From question 1 file
    result = 1
    base %= modulus
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulus
        base = (base * base) % modulus
        exponent //= 2
    return result

def elgamal_keygen(p, g):
    private = random.randint(2, p - 2)
    h = mod_exp(g, private, p)
    return (p, g, h), private

# ElGamal Encryption
def elgamal_encrypt(m, p, g, h):
    k = random.randint(2, p - 2)
    c1 = mod_exp(g, k, p)
    s = mod_exp(h, k, p)
    c2 = (m * s) % p
    return c1, c2

# ElGamal Decryption
def elgamal_decrypt(c1, c2, x, p):
    s = mod_exp(c1, x, p)
    s_inv = mod_inverse(s, p)
    m = (c2 * s_inv) % p
    return m

# Encrypt and Decrypt Strings
def encrypt_string(message, public_key):
    p, g, h = public_key
    out = []
    for ch in message:
        m = ord(ch)
        c1, c2 = elgamal_encrypt(m, p, g, h)
        out.append((c1, c2))
    return out

def decrypt_string(ciphertext_list, private_key, p):
    result = []
    for c1, c2 in ciphertext_list:
        m = elgamal_decrypt(c1, c2, private_key, p)
        result.append(chr(m))
    return "".join(result)

if __name__ == "__main__":
    p = 31847
    g = 5

    # 1. Key generation
    public_key, private_key = elgamal_keygen(p, g)
    p_pub, g_pub, h_pub = public_key

    print("=== ElGamal over Integers (Question 3) ===")
    print(f"Prime p        : {p_pub}")
    print(f"Generator g    : {g_pub}")
    print(f"Public key h   : {h_pub}")
    print(f"Private key x  : {private_key}")
    print()

    # 2. Message to encrypt
    message = "RETREAT AT 0900"
    print(f"Original message: {message}")

    # 3. Encrypted message
    ciphertexts = encrypt_string(message, public_key)
    print("\nCiphertexts (per character):")
    for i, (c1, c2) in enumerate(ciphertexts):
        print(f"  char[{i}] = '{message[i]}'  ->  (c1={c1}, c2={c2})")

    # 4. Decrypt back
    decrypted_message = decrypt_string(ciphertexts, private_key, p)
    print("\nDecrypted message:", decrypted_message)

    # 5. Verify
    print("\nDecryption successful:", decrypted_message == message)
