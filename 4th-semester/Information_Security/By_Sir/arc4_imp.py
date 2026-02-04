def arc4crypt(data: bytes, key: bytes) -> bytes:
    x = 0
    box = list(range(256))
    for i in range(256):
        x = (x + box[i] + key[i % len(key)]) % 256
        box[i], box[x] = box[x], box[i]

    x = y = 0
    out = bytearray()
    for byte in data:
        x = (x + 1) % 256
        y = (y + box[x]) % 256
        box[x], box[y] = box[y], box[x]
        out.append(byte ^ box[(box[x] + box[y]) % 256])
    return bytes(out)


key = b'SuperSecretKey!!'
origtext = b'Dive Dive Dive'
ciphertext = arc4crypt(origtext, key)
plaintext = arc4crypt(ciphertext, key)
print('The original text is: {}'.format(origtext))
print('The ciphertext is: {}'.format(ciphertext.hex().upper()))
print('The plaintext is: {}'.format(plaintext))