# Lab Activity 3: ROT-13 Cipher

# We make a shoft of 3 in Caesar and of 13 in ROT-13 Cipher

key = 'abcdefghijklmnopqrstuvwxyz'

def enc_caesar(n, plaintext):
    result = ''
    for l in plaintext.lower():
        try:
            i = (key.index(l) + n) % 26 
            result += key[i]
        except ValueError: 
            result += l 
    return result 

plaintext = 'We hold these truths to be self-evident, that all men are created equal.'
print("Original:", plaintext)
ciphertext = enc_caesar(13, plaintext) 
print("Ciphertext:", ciphertext)

def dec_caesar(n, ciphertext):
    result = ''
    for l in ciphertext:
        try: 
            i = (key.index(l) - n) % 26 
            result += key[i] 
        except ValueError:
            result += l
    return result 

# ciphertext = 'zh krog wkhvh wuxwkv wr eh vhoi-hylghqw, wkdw doo phq duh fuhdwhg htxdo.' # Caesar
# ciphertext = 'jr ubyq gurfr gehguf gb or frys-rivqrag, gung nyy zra ner perngrq rdhny.' # ROT-13
plaintext = dec_caesar(13, ciphertext)
print("Decrypted:", plaintext)
