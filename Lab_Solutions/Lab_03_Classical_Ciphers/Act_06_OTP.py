# Lab Activity 5: One-Time Pad Function
import secrets

# # you can generate a key equal to the length of the message using the following:
# msg = "helloworldthisistheonetimepad" 
# key = '' 
# for i in range(len(msg)):
#     key += secrets.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') # Use uppercase letters 
# print("Key:",key)

def key_generation(length):
    """ Generates a random binary key of a given length. """ 
    return ''.join(secrets.choice('01')
                   for _ in range(length)) 
    
def xor_operation(binary_str1, binary_str2): 
    """ Performs bitwise XOR between two binary strings. """ 
    return ''.join(str(int(a) ^ int(b))
                   for a, b in zip(binary_str1, binary_str2))

def encrypt(key, message):
    """ Encrypts the message using the one-time pad encryption (XOR operation). """
    return xor_operation(key, message) 

def decrypt(key, ciphertext):
    """ Decrypts the ciphertext using the one-time pad decryption (XOR operation). """
    return xor_operation(key, ciphertext)

# Test the one-time pad algorithm
str_len = 10 # Length of the binary string (can be set to any desired length)
message = ''.join(secrets.choice('01') for _ in range(str_len)) # Generate a random binary message

# Key generation
key = key_generation(str_len)
# Encryption
ciphertext = encrypt(key, message)
# Decryption 
decrypted_message = decrypt(key, ciphertext) 
# Display the results
print("Message: ", message) 
print("Key: ", key) 
print("Ciphertext: ", ciphertext) 
print("Decrypted Text: ", decrypted_message) 
# Ensure the decrypted message matches the original 
assert decrypted_message == message, "Decryption failed! The original message and decrypted message don't match."
