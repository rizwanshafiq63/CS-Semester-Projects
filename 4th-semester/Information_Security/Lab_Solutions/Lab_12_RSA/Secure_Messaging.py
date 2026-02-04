""" 
Practical RSA Implementation for Secure Messaging 
Demonstrates: Key generation, encryption, decryption, signing, verification 
""" 
from RSA_Signature import RSASignature
from RSA import RSA

class SecureMessaging: 
    """ 
    Complete secure messaging system using RSA 
    """ 
    def __init__(self): 
        self.rsa = RSA() 
        self.users = {}  # Store user public keys 

    def register_user(self, username, bits=512): 
        """ 
        Register a new user with RSA key pair 
        """ 
        print(f"\nRegistering user: {username}") 
        public_key, private_key = self.rsa.generate_keypair(bits) 
        # Store public key in directory (like a PKI) 
        self.users[username] = { 
            'public_key': public_key, 
            'private_key': private_key  # Normally user keeps this secret! 
        } 
        print(f"User {username} registered") 
        return public_key, private_key 

    def send_secure_message(self, sender, receiver, message):
        """ 
        Send encrypted and signed message 
        """ 
        print(f"\n{'='*60}") 
        print(f"{sender} sending message to {receiver}") 
        print(f"{'='*60}") 
        # Get keys 
        sender_private = self.users[sender]['private_key'] 
        receiver_public = self.users[receiver]['public_key'] 
        print(f"\n1. Original Message: '{message}'") 
        # Convert message to numbers (simple approach: ASCII values) 
        message_numbers = [ord(c) for c in message] 
        print(f"2. As numbers: {message_numbers}") 
        # Encrypt each character with receiver's public key 
        encrypted = [] 
        for num in message_numbers: 
            if num < receiver_public[0]:  # Check if fits in modulus 
                cipher = self.rsa.encrypt(num, receiver_public) 
                encrypted.append(cipher) 
        print(f"3. Encrypted: {encrypted[:5]}..." if len(encrypted) > 5 else f"3. Encrypted: {encrypted}") 
        # Sign the original message with sender's private key 
        sig_system = RSASignature(self.rsa) 
        signature = sig_system.sign(message, sender_private) 
        print(f"4. Digital Signature: {signature}") 
        # Package: (encrypted_message, signature) 
        package = (encrypted, signature) 
        print("\nMessage packaged and ready to send") 
        return package 

    def receive_secure_message(self, sender, receiver, package): 
        """ 
        Receive, verify, and decrypt message
        """ 
        print(f"\n{'='*60}") 
        print(f"{receiver} receiving message from {sender}") 
        print(f"{'='*60}") 
        encrypted, signature = package 
        # Get keys 
        receiver_private = self.users[receiver]['private_key'] 
        sender_public = self.users[sender]['public_key'] 
        print("\n1. Received encrypted message and signature") 
        # Decrypt message with receiver's private key 
        decrypted_numbers = [] 
        for cipher in encrypted: 
            num = self.rsa.decrypt(cipher, receiver_private) 
            decrypted_numbers.append(num) 
        decrypted_message = ''.join([chr(n) for n in decrypted_numbers]) 
        print(f"2. Decrypted message: '{decrypted_message}'") 
        # Verify signature with sender's public key 
        sig_system = RSASignature(self.rsa) 
        is_valid = sig_system.verify(decrypted_message, signature, sender_public) 
        print(f"3. Signature verification: {is_valid}") 
        if is_valid: 
            print(f"\nMessage authenticated - Sender is {sender}") 
            print("Message integrity verified - Not tampered") 
            return decrypted_message 
        else: 
            print("\nWARNING: Signature invalid - Message may be forged!") 
            return None 

# Complete Demonstration 
def main_demo(): 
    """ 
    Complete demonstration of secure messaging system 
    """ 
    print("="*60) 
    print("SECURE MESSAGING SYSTEM DEMONSTRATION") 
    print("="*60) 
    # Create messaging system 
    system = SecureMessaging() 
    # Register Alice and Bob 
    alice_public, alice_private = system.register_user("Alice", bits=512) 
    bob_public, bob_private = system.register_user("Bob", bits=512) 
    # Alice sends message to Bob 
    message = "Meet at 3pm" 
    package = system.send_secure_message("Alice", "Bob", message) 
    # Bob receives and verifies 
    received = system.receive_secure_message("Alice", "Bob", package) 
    print(f"\n{'='*60}") 
    print("RESULT") 
    print(f"{'='*60}") 
    print(f"Original:  '{message}'") 
    print(f"Received:  '{received}'") 
    print(f"Match: {message == received} ") 

if __name__ == "__main__": 
    main_demo()