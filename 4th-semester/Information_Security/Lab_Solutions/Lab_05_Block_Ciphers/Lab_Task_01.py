from Crypto.Cipher import DES 
from Crypto.Random import get_random_bytes 
from Crypto.Util.Padding import pad, unpad 

# DES key must be exactly 8 bytes long 
key = get_random_bytes(8) 

def des_encrypt(data, key): 
    cipher = DES.new(key, DES.MODE_ECB) 
    padded_data = pad(data, DES.block_size) 
    encrypted_data = cipher.encrypt(padded_data) 
    return encrypted_data 

def des_decrypt(encrypted_data, key): 
    cipher = DES.new(key, DES.MODE_ECB) 
    decrypted_data = unpad(cipher.decrypt(encrypted_data), DES.block_size) 
    return decrypted_data 

# Example usage 
if __name__ == "__main__": 
    # Input data (must be bytes) 
    data = b"Secret123" 

    print(f"Original Data: {data}") 

    # Encrypt the data 
    encrypted_data = des_encrypt(data, key) 
    print(f"Encrypted Data: {encrypted_data}") 

    # Decrypt the data 
    decrypted_data = des_decrypt(encrypted_data, key) 
    print(f"Decrypted Data: {decrypted_data}") 
