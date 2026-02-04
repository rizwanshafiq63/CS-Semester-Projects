# Function to shift a character by n positions in the alphabet
def shift_enc(c, n):
    return chr(((ord(c.upper()) - ord('A') + n) % 26) + ord('A'))


# Function to convert keyword into numeric key
def key_vigenere(key):
    key_array = []
    for i in range(len(key)):
        key_element = ord(key[i].upper()) - ord('A')  # Convert A=0, B=1, ...
        key_array.append(key_element)
    return key_array


# Function to encrypt plaintext with Vigenère cipher
def enc_vigenere(plaintext, key):
    secret = ""
    for i in range(len(plaintext)):
        if plaintext[i].isalpha():
            secret += shift_enc(plaintext[i], key[i % len(key)])
        else:
            secret += plaintext[i]
    return secret


# Function to decrypt ciphertext (reverse shifting)
def dec_vigenere(ciphertext, key):
    plain = ""
    for i in range(len(ciphertext)):
        if ciphertext[i].isalpha():
            plain += shift_enc(ciphertext[i], - key[i % len(key)])  # negative shift
        else:
            plain += ciphertext[i]
    return plain


# Example
secretKey = 'DECLARATION'
key = key_vigenere(secretKey)
print("Numeric key:", key)

plaintext = 'ALL MEN ARE, CREATED EQUAL'
ciphertext = enc_vigenere(plaintext, key)
print("Plaint text: ", plaintext)
print("Ciphertext:", ciphertext)

decrypted = dec_vigenere(ciphertext, key)
print("Decrypted:", decrypted)