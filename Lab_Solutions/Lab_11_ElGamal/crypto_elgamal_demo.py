# Using PyCryptodome library
from Crypto.PublicKey import ElGamal
from Crypto.Random import get_random_bytes
from Crypto.Hash import SHA256

# Generate keys (2048-bit security)
key = ElGamal.generate(2048, get_random_bytes)

# Export public key
public_key = key.publickey().exportKey()

# Encrypt message
message = b"Secret message"
k = get_random_bytes(32)      # Random value
ciphertext = key.encrypt(message, k)

# Decrypt
plaintext = key.decrypt(ciphertext)

print(f"Original: {message}")
print(f"Decrypted: {plaintext}")
