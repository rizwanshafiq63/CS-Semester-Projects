import random

def mod_exp(base, exp, mod): 
    """ 
    Efficient modular exponentiation using binary method 
    Computes (base^exp) % mod 
    """ 
    result = 1 
    base = base % mod 
    while exp > 0: 
        if exp % 2 == 1:  # If exp is odd 
            result = (result * base) % mod 
        exp = exp >> 1     # Divide exp by 2 
        base = (base * base) % mod 
    return result

def mod_inverse(a, p): 
    """ 
    Compute modular inverse using Fermat's Little Theorem 
    For prime p: a^(-1) ≡ a^(p-2) (mod p) 
    """ 
    return mod_exp(a, p - 2, p)

def is_primitive_root(g, p):
    """
    Check if g is a primitive root modulo p.
    A primitive root generates all elements in Z*_p.
    Args:
        g: Potential generator
        p: Prime modulus
    Returns:
        True if g is a primitive root, False otherwise
    """
    # Check if g^((p-1)/q) != 1 for all prime factors q of p-1
    # Simplified check: generate all powers and check if we get p-1 distinct values
    if g <= 1 or g >= p:
        return False
    seen = set()
    power = 1
    for i in range(1, p):
        power = (power * g) % p
        if power in seen:
            return False
        seen.add(power)
    return len(seen) == p - 1

class ElGamal: 
    def __init__(self, p, g): 
        """ 
        Initialize ElGamal with prime p and generator g 
        """ 
        self.p = p  # Large prime 
        self.g = g  # Generator
        # Validate inputs
        if not is_primitive_root(g, p):
            raise ValueError(f"{g} is not a primitive root modulo {p}")
        if self.p < 3:
            raise ValueError("Prime p must be at least 3")
        if self.g < 2 or self.g >= self.p:
            raise ValueError(f"Generator g must be between 2 and {self.p - 1}")

    def generate_keys(self): 
        """ 
        Generate public and private key pair
        Returns: (public_key, private_key) 
        """ 
        # Choose random private key x 
        x = random.randint(2, self.p - 2) 
        # Compute public key y = g^x mod p 
        y = mod_exp(self.g, x, self.p) 
        public_key = (self.p, self.g, y) 
        private_key = x 
        return public_key, private_key 

    def encrypt(self, message, public_key): 
        """ 
        Encrypt a message using public key 
        Args: 
            message: integer message (M < p)
            public_key: tuple (p, g, y) 
        Returns: ciphertext tuple (C1, C2) 
        """ 
        p, g, y = public_key
        # Validate message
        if message < 0 or message >= p:
            raise ValueError(f"Message must be in range [0, {p-1}]")
        # Choose random k 
        k = random.randint(2, p - 2) 
        # Compute C1 = g^k mod p 
        C1 = mod_exp(g, k, p) 
        # Compute C2 = M * y^k mod p 
        C2 = (message * mod_exp(y, k, p)) % p 
        return (C1, C2) 

    def decrypt(self, ciphertext, private_key): 
        """ 
        Decrypt ciphertext using private key
        Args: 
            ciphertext: tuple (C1, C2) 
            private_key: integer x 
        Returns: original message M 
        """ 
        C1, C2 = ciphertext 
        # Compute s = C1^x mod p 
        s = mod_exp(C1, private_key, self.p) 
        # Compute s^(-1) mod p 
        s_inv = mod_inverse(s, self.p) 
        # Recover message M = C2 * s^(-1) mod p 
        message = (C2 * s_inv) % self.p 
        return message 

    def encrypt_string(self, text, public_key):
        """
        Encrypt a string message by converting to integers.
        Args:
            text: String message to encrypt
            public_key: tuple (p, g, y)
        Returns:
            list: List of ciphertext pairs [(C1, C2), ...]
        """
        ciphertexts = []
        for char in text:
            # Convert character to ASCII value
            ascii_val = ord(char)
            # Encrypt the ASCII value
            ciphertext = self.encrypt(ascii_val, public_key)
            ciphertexts.append(ciphertext)
        return ciphertexts
    
    def decrypt_string(self, ciphertexts, private_key):
        """
        Decrypt a list of ciphertexts back to string.
        Args:
            ciphertexts: List of ciphertext pairs
            private_key: integer x
        Returns:
            str: Decrypted message
        """
        message = ""
        for ciphertext in ciphertexts:
            # Decrypt to get ASCII value
            ascii_val = self.decrypt(ciphertext, private_key)
            # Convert ASCII to character
            message += chr(ascii_val)
        return message

# ============================================================
# Demonstration and Testing
# ============================================================

def demonstrate_elgamal():
    """
    Comprehensive demonstration of ElGamal encryption system.
    """
    print("=" * 60)
    print("ELGAMAL ENCRYPTION SYSTEM DEMONSTRATION")
    print("=" * 60)

    # Initialize with small prime for demonstration
    p = 23
    g = 5
    elgamal = ElGamal(p, g)

    print("\nSystem Parameters:")
    print(f"  Prime (p): {p}")
    print(f"  Generator (g): {g}")

    # Generate keys
    print("\n" + "-" * 60)
    print("KEY GENERATION")
    print("-" * 60)

    public_key, private_key = elgamal.generate_keys()
    p_pub, g_pub, y_pub = public_key

    print("Public Key:")
    print(f"  p = {p_pub}")
    print(f"  g = {g_pub}")
    print(f"  y = {y_pub}")
    print("\nPrivate Key:")
    print(f"  x = {private_key}")

    # Encrypt a message
    print("\n" + "-" * 60)
    print("ENCRYPTION")
    print("-" * 60)

    message = 19
    print(f"Original Message: {message}")

    ciphertext = elgamal.encrypt(message, public_key)
    C1, C2 = ciphertext

    print("Ciphertext:")
    print(f"  C1 = {C1}")
    print(f"  C2 = {C2}")

    # Decrypt the message
    print("\n" + "-" * 60)
    print("DECRYPTION")
    print("-" * 60)

    decrypted = elgamal.decrypt(ciphertext, private_key)
    print(f"Decrypted Message: {decrypted}")

    # Verify
    if message == decrypted:
        print("\n  SUCCESS! Encryption/Decryption verified.")
    else:
        print("\n  ERROR! Messages don’t match.")

    # Demonstrate probabilistic encryption
    print("\n" + "-" * 60)
    print("PROBABILISTIC ENCRYPTION PROPERTY")
    print("-" * 60)
    print("Encrypting the same message multiple times:\n")

    for i in range(1, 4):
        ct = elgamal.encrypt(message, public_key)
        print(f"  Encryption {i}: {ct}")

    print("\nNote: Different ciphertexts for the same message!")
    print("This is semantic security in action.")


# Run demonstration
if __name__ == "__main__":
    demonstrate_elgamal()

