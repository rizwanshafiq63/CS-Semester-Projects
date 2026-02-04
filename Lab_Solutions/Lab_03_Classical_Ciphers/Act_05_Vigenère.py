# Lab Activity 5: Vigenère Cipher

# Used in encryption and decryption
def key_vigenere(key):
    keyArray = []
    for i in range(0, len(key)):
        keyElement = ord(key[i].upper()) - 65 # Ensure uppercase
        keyArray.append(keyElement)
    return keyArray

# Encryption
def shiftEnc(c, n): 
    if c.isalpha(): 
        return chr(((ord(c) - ord('A') + n) % 26) + ord('A'))
    else:
        return c # Keep non-alphabet characters unchanged 

def enc_vigenere(plaintext, key): 
    secret = "".join([shiftEnc(plaintext[i], key[i % len(key)])
                      if plaintext[i].isalpha()
                      else plaintext[i] 
                      for i in range(len(plaintext))]) 
    return secret

secretKey = 'DECLARATION' 
key = key_vigenere(secretKey) 
print("Key: ",key)
plaintext = 'ALL MEN ARE CREATED EQUAL'
print("Plaintext:", plaintext) 
ciphertext = enc_vigenere(plaintext, key)
print("Ciphertext:",ciphertext)

# Decryption
def shiftDec(c, n):
    if c.isalpha():
        c = c.upper()
        return chr(((ord(c) - ord('A') - n) % 26) + ord('A')) 
    else:
        return c # Return non-alphabetic characters unchanged 

def dec_vigenere(ciphertext, key):
    plain = "".join([shiftDec(ciphertext[i], key[i % len(key)])
                     if ciphertext[i].isalpha()
                     else ciphertext[i]
                     for i in range(len(ciphertext))]) 
    return plain

decoded = dec_vigenere(ciphertext, key) 
print("Decoded Text:",decoded)
