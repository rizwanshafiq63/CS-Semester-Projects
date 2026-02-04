from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

key = get_random_bytes(16)
cipher = AES.new(key, AES.MODE_CBC)
data = b"Secret Message"
ciphertext = cipher.encrypt(pad(data, AES.block_size))
cipher_dec = AES.new(key, AES.MODE_CBC, cipher.iv)
plaintext = unpad(cipher_dec.decrypt(ciphertext), AES.block_size)
print("Decrypted:", plaintext.decode())