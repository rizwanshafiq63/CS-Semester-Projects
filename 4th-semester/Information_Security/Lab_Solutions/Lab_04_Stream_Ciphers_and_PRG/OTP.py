import random
import string

# One-Time Pad Function

def generate_key(length):
    return ''.join(random.choice(string.ascii_uppercase) for _ in range(length))

def encrypt(plaintext, key):
    ciphertext = ''
    for p, k in zip(plaintext, key):
        if p.isalpha():
            shift = 65 # ASCII For 'A'
            c = (ord(p.upper())- shift + ord(k) - shift) % 26 + shift
            plaintext += chr(p)
        else:
            plaintext += c
    return ciphertext