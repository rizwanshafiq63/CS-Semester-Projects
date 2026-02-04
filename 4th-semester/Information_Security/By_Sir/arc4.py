def arc4crypt(plaintext, key):
    j = 0
    S = list(range(256)) # Ensure S is a list, not range object
    # Key-scheduling algorithm (KSA)
    for i in range(256):
        j = (j + S[i] + ord(key[i % len(key)])) % 256
        S[i], S[j] = S[j], S[i] # Swap values

    x = 0
    y = 0
    keystream = []
    # Pseudo-random generation algorithm (PRGA)
    for char in plaintext:
        x = (x + 1) % 256
        y = (y + S[x]) % 256
        S[x], S[y] = S[y], S[x] # Swap values
        keystream.append(chr(ord(char) ^ S[(S[x] + S[y]) % 256])) # XOR with keystream
    return ''.join(keystream)


# Testing the ARC4 encryption and decryption
key = 'SUN'
origtext = 'Hello World!'
ciphertext = arc4crypt(origtext, key)
plaintext = arc4crypt(ciphertext, key)
print('The original text is: {}'.format(origtext))
print('The ciphertext is: {}'.format(ciphertext))
print('The plaintext is: {}'.format(plaintext))