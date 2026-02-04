import secrets

def generate_key(length):
    """Generate a random key of given length using secrets (uppercase A-Z)."""
    return ''.join(secrets.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(length))

def encrypt(plaintext, key):
    """Encrypt plaintext using XOR with the key."""
    ciphertext = ""
    for p, k in zip(plaintext, key):
        c = chr(ord(p) ^ ord(k))  # XOR of ASCII codes
        ciphertext += c
    return ciphertext

def decrypt(ciphertext, key):
    """Decrypt ciphertext using XOR with the key."""
    plaintext = ""
    for c, k in zip(ciphertext, key):
        p = chr(ord(c) ^ ord(k))
        plaintext += p
    return plaintext

# Example usage
plaintext = "HELLO"
key = generate_key(len(plaintext))
ciphertext = encrypt(plaintext, key)
decrypted = decrypt(ciphertext, key)

print("Plaintext :", plaintext)
print("Key       :", key)
print("Ciphertext (raw):", ciphertext)
print("Ciphertext (as bytes):", [ord(x) for x in ciphertext])
print("Decrypted :", decrypted)
