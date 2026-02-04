# Task 01: Affine Cipher Implementation

# Function to compute gcd
def gcd(a, b):
    while b != 0:
        # a, b = b, a % b
        temp_a = b
        temp_b = a % b
        a = temp_a
        b = temp_b
    return a

# Function to find modular inverse of a under mod m
def mod_inverse(a, m):
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

# Encryption: (A*x + B) mod m
def affine_encrypt(text, A, B):
    result = ""
    m = 26  # alphabet size
    for char in text.upper():
        if char.isalpha():
            x = ord(char) - ord('A')
            enc = (A * x + B) % m
            result += chr(enc + ord('A'))
        else:
            result += char
    return result

# Decryption: A^-1 * (y - B) mod m
def affine_decrypt(cipher, A, B):
    result = ""
    m = 26
    A_inv = mod_inverse(A, m)
    if A_inv is None:
        return "Error: No modular inverse for given A"
    
    for char in cipher.upper():
        if char.isalpha():
            y = ord(char) - ord('A')
            dec = (A_inv * (y - B)) % m
            result += chr(dec + ord('A'))
        else:
            result += char
    return result

# ------------------- Example -------------------
A = 5  # Key A (must be coprime with 26)
B = 8  # Key B
plaintext = "AFFINE CIPHER"

print("Plaintext:", plaintext)

ciphertext = affine_encrypt(plaintext, A, B)
print("Encrypted:", ciphertext)

decrypted = affine_decrypt(ciphertext, A, B)
print("Decrypted:", decrypted)
