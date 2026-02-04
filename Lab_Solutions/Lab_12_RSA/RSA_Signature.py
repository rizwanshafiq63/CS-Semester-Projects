import hashlib 
from RSA import RSA

class RSASignature: 
    """ 
    RSA Digital Signature Implementation 
    """ 
    def __init__(self, rsa_instance): 
        self.rsa = rsa_instance 

    def hash_message(self, message): 
        """ 
        Create hash of message using SHA-256
        Returns integer representation 
        """ 
        if isinstance(message, str): 
            message = message.encode() 
        hash_obj = hashlib.sha256(message) 
        hash_hex = hash_obj.hexdigest() 
        hash_int = int(hash_hex, 16) 
        return hash_int 

    def sign(self, message, private_key): 
        """ 
        Sign a message using private key 
        Args: 
            message: string or bytes to sign
            private_key: (n, d) 
        Returns: signature S 
        """ 
        n, d = private_key 
        # Hash the message 
        h = self.hash_message(message) 
        # Reduce hash to fit within modulus 
        h = h % n 
        # Sign: S = h^d mod n 
        signature = pow(h, d, n) 
        return signature 

    def verify(self, message, signature, public_key): 
        """ 
        Verify a signature using public key 
        Args: 
            message: original message 
            signature: S to verify 
            public_key: (n, e) 
        Returns: True if valid, False otherwise 
        """ 
        n, e = public_key 
        # Hash the message 
        h = self.hash_message(message) 
        h = h % n 
        # Verify: h' = S^e mod n 
        h_prime = pow(signature, e, n) 
        # Check if hashes match 
        return h == h_prime 

# Demonstration 
def demonstrate_signatures(): 
    """ 
    Demonstrate RSA digital signatures 
    """ 
    print("\n" + "="*60) 
    print("RSA DIGITAL SIGNATURE DEMONSTRATION") 
    print("="*60)

    # Setup RSA 
    rsa = RSA() 
    public_key, private_key = rsa.generate_keypair(bits=512) 

    sig_system = RSASignature(rsa) 

    # Original message 
    message = "This is an important contract." 
    print(f"\nOriginal Message: '{message}'") 

    # Alice signs the message 
    signature = sig_system.sign(message, private_key) 
    print(f"\nSignature (Alice's private key): {signature}") 

    # Bob verifies the signature 
    is_valid = sig_system.verify(message, signature, public_key) 
    print(f"\nVerification (Alice's public key): {is_valid}") 

    if is_valid: 
        print("Signature is VALID - Message is authentic!") 

    # Try tampering with message 
    print("\n" + "-"*60) 
    print("TAMPERING TEST") 
    print("-"*60) 
    tampered_message = "This is an important contract!"  # Added '!' 
    print(f"\nTampered Message: '{tampered_message}'") 
    is_valid_tampered = sig_system.verify(tampered_message, signature, public_key) 
    print(f"Verification: {is_valid_tampered}") 
    if not is_valid_tampered: 
        print("Tampering detected - Signature INVALID!") 

# Run signature demonstration 
if __name__ == "__main__": 
    demonstrate_signatures()
