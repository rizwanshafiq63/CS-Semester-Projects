key = "abcdefghijklmnopqrstuvwxyz"

def encrypt(plaintext, shift):
    ciphertext = ""
    for letter in plaintext.lower():
        try:
            c = (key.index(letter) + shift) % 26
            ciphertext += key[c]

        except:
            ciphertext += letter

    return ciphertext

def decrypt(ciphertext, shift):
    plaintext = ""
    for letter in ciphertext.lower():
        try:
            c = (key.index(letter) - shift) % 26
            plaintext += key[c]

        except:
            plaintext += letter

    return plaintext

plainttxt = "Hello World"
print("Plaint text: ", plainttxt)
shift = 13

ciphertxt = encrypt(plainttxt, shift)

print("Cipher text: ", ciphertxt)

plaint = decrypt(ciphertxt, shift)

print("Plain: ", plaint)


"003"