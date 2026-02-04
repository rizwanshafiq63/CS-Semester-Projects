
def mod_inverse(a, m):
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

# Encryption: (A*x + B) mod m
def affine_encrypt(text, A, B):
    result = ""
    m = 26  
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


A = 5  
B = 8  
plaintext = "AFFINE CIPHER"

print("Plaintext:", plaintext)

ciphertext = affine_encrypt(plaintext, A, B)
print("Encrypted:", ciphertext)

decrypted = affine_decrypt(ciphertext, A, B)
print("Decrypted:", decrypted)