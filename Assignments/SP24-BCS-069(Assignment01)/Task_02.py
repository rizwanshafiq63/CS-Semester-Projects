
def mod_inverse(a, m):
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

# Encryption (C = (P × k) mod m)
def multiplicative_encrypt(plaintext, key):
    ciphertext = ''
    for char in plaintext.upper():
        if char.isalpha():
            num = ord(char) - ord('A')
            enc = (num * key) % 26
            ciphertext += chr(enc + ord('A'))
        else:
            ciphertext += char
    return ciphertext

# Decryption (P = (C × k^−1) mod m)
def multiplicative_decrypt(ciphertext, key):
    plaintext = ''
    inv_key = mod_inverse(key, 26)
    if inv_key is None:
        return "Error: No modular inverse for given key!"
    
    for char in ciphertext.upper():
        if char.isalpha():
            num = ord(char) - ord('A')
            dec = (num * inv_key) % 26
            plaintext += chr(dec + ord('A'))
        else:
            plaintext += char
    return plaintext


key = 7 
plaintext = "HELLO WORLD"

print("Plaintext:", plaintext)

ciphertext = multiplicative_encrypt(plaintext, key)
print("Ciphertext:", ciphertext)

decrypted = multiplicative_decrypt(ciphertext, key)
print("Decrypted:", decrypted)


def hack_multiplicative(ciphertext):
    # Since key must be coprime with 26, there are only 12 possible keys
    # because 26 = 2 * 13, what it means is that key should not be divisible by 2 or 13
    possible_keys = [1,3,5,7,9,11,15,17,19,21,23,25]
    for k in possible_keys:
        print(f"Trying key {k}: {multiplicative_decrypt(ciphertext, k)}")
    # From the results, the user can identify the correct plaintext.

hack_multiplicative(ciphertext)