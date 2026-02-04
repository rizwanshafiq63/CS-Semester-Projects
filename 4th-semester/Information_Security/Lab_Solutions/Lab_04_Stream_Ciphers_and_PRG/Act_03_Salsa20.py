from nacl.secret import SecretBox 
from nacl.utils import random 
 
# The key must be 32 bytes for XSalsa20 
key = b'*secret**secret**secret**secret*' 
 
# Create a SecretBox, which uses XSalsa20 internally 
box = SecretBox(key) 
 
# The nonce must be 24 bytes for XSalsa20 
nonce = random(24) 
 
# Encrypting the message 
message = b"IT'S A YELLOW SUBMARINE" 
ciphertext = box.encrypt(message, nonce) 
 
# Decrypting the message 
decrypted = box.decrypt(ciphertext) 
 
print(decrypted.decode())  # Should output: IT'S A YELLOW SUBMARINE
