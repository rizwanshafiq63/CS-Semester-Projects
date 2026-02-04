def VernamEncDec(text, key): 
    result = "" 
    ptr = 0 
    for char in text: 
        result += chr(ord(char) ^ ord(key[ptr]))  # XOR each character with the key 
        ptr += 1 
        if ptr == len(key):  # Reset the key pointer if it reaches the end of the key 
            ptr = 0 
    return result 

# Key for Vernam Cipher 
key = "thisismykey12345"

while True: 
    input_text = input("\nEnter Text To Encrypt:\t") 
    # Encrypt the input text 
    ciphertext = VernamEncDec(input_text, key) 
    print("\nEncrypted Vernam Cipher Text:\t" + ciphertext) 
    # Decrypt the ciphertext 
    plaintext = VernamEncDec(ciphertext, key) 
    print("\nDecrypted Vernam Cipher Text:\t" + plaintext) 
    if input("\nDo you want to continue? (y/n): ").lower() != 'y': 
        break
