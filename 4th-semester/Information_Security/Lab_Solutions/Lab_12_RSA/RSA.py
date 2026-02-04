import random 

class RSA: 
    """ 
    RSA Cryptosystem Implementation 
    """

    def __init__(self): 
        self.public_key = None 
        self.private_key = None

    def gcd(self, a, b): 
        """ 
        Compute Greatest Common Divisor using Euclidean Algorithm 
        """ 
        while b: 
            a, b = b, a % b 
        return a 

    def extended_gcd(self, a, b): 
        """ 
        Extended Euclidean Algorithm 
        Returns (gcd, x, y) where ax + by = gcd 
        """ 
        if b == 0: 
            return a, 1, 0 
        else: 
            gcd, x1, y1 = self.extended_gcd(b, a % b) 
            x = y1 
            y = x1 - (a // b) * y1 
            return gcd, x, y 

    def mod_inverse(self, e, phi): 
        """ 
        Compute modular multiplicative inverse of e modulo phi 
        Find d such that (e × d) ≡ 1 (mod phi) 
        """ 
        gcd, x, y = self.extended_gcd(e, phi) 
        if gcd != 1: 
            raise ValueError("Modular inverse does not exist") 
        # Make sure d is positive 
        return (x % phi + phi) % phi 

    def is_prime(self, n, k=5): 
        """ 
        Miller-Rabin Primality Test 
        Args: 
            n: number to test 
            k: number of rounds (higher = more accurate) 
        Returns: True if probably prime, False if composite 
        """ 
        if n < 2: 
            return False 
        if n == 2 or n == 3: 
            return True 
        if n % 2 == 0: 
            return False 
        # Write n-1 as 2^r × d 
        r, d = 0, n - 1 
        while d % 2 == 0: 
            r += 1 
            d //= 2 
        # Witness loop 
        for _ in range(k): 
            a = random.randrange(2, n - 1) 
            x = pow(a, d, n) 
            if x == 1 or x == n - 1: 
                continue 
            for _ in range(r - 1): 
                x = pow(x, 2, n) 
                if x == n - 1: 
                    break 
            else: 
                return False 
        return True 

    def generate_prime(self, bits=16): 
        """ 
        Generate a random prime number with specified bit length 
        Note: Using small bits for demonstration; use 1024+ for real security 
        """ 
        while True: 
            # Generate random odd number 
            num = random.getrandbits(bits) 
            num |= (1 << bits - 1) | 1  # Set MSB and LSB to 1 
            if self.is_prime(num): 
                return num 

    def generate_keypair(self, bits=16):
        """ 
        Generate RSA public and private key pair 
        Args: 
            bits: bit length for primes (use 1024+ for real security) 
        Returns: ((n, e), (n, d)) - public and private keys 
        """ 
        print(f"\n{'='*60}") 
        print(f"GENERATING RSA KEYS ({bits}-bit primes)") 
        print(f"{'='*60}") 
        # Step 1: Generate two distinct primes 
        print("\nStep 1: Generating prime p...") 
        p = self.generate_prime(bits) 
        print(f"  p = {p}") 
        print("\nStep 2: Generating prime q...") 
        q = self.generate_prime(bits) 
        while q == p:  # Ensure p ≠ q 
            q = self.generate_prime(bits) 
        print(f"  q = {q}") 
        # Step 2: Compute n = p × q 
        n = p * q 
        print("\nStep 3: Computing n = p × q") 
        print(f"  n = {n}") 
        # Step 3: Compute φ(n) 
        phi = (p - 1) * (q - 1) 
        print("\nStep 4: Computing φ(n) = (p-1)(q-1)") 
        print(f"  φ(n) = {phi}") 
        # Step 4: Choose e (commonly 65537) 
        e = 65537 
        # If e doesn't work, find another 
        if e >= phi or self.gcd(e, phi) != 1: 
            e = 3 
            while self.gcd(e, phi) != 1: 
                e += 2 
        print("\nStep 5: Choosing public exponent e") 
        print(f"  e = {e}") 
        print(f"  gcd(e, φ(n)) = {self.gcd(e, phi)}") 
        # Step 5: Compute d (modular inverse of e) 
        d = self.mod_inverse(e, phi) 
        print("\nStep 6: Computing private exponent d") 
        print(f"  d = {d}") 
        print(f"  Verification: (e × d) mod φ(n) = {(e * d) % phi}") 
        # Store keys 
        self.public_key = (n, e) 
        self.private_key = (n, d) 
        print(f"\n{'='*60}") 
        print("✓ KEY GENERATION COMPLETE") 
        print(f"{'='*60}") 
        print(f"Public Key:  (n={n}, e={e})") 
        print(f"Private Key: (n={n}, d={d})") 
        return self.public_key, self.private_key 

    def encrypt(self, message, public_key): 
        """ 
        Encrypt message using RSA public key
        Args: 
            message: integer message (M < n)
            public_key: tuple (n, e) 
        Returns: ciphertext C 
        """ 
        n, e = public_key 
        if message >= n: 
            raise ValueError(f"Message {message} must be less than n={n}") 
        # C = M^e mod n 
        ciphertext = pow(message, e, n) 
        return ciphertext 

    def decrypt(self, ciphertext, private_key): 
        """ 
        Decrypt ciphertext using RSA private key 
        Args: 
            ciphertext: encrypted message C 
            private_key: tuple (n, d) 
        Returns: original message M 
        """ 
        n, d = private_key 
        # M = C^d mod n 
        message = pow(ciphertext, d, n) 
        return message 

    def encrypt_string(self, text, public_key): 
        """ 
        Encrypt a text string (character by character) 
        """ 
        n, e = public_key 
        encrypted = [] 
        for char in text: 
            m = ord(char)  # Convert to ASCII 
            if m >= n: 
                raise ValueError(f"Character '{char}' (ASCII {m}) too large for n= {n}") 
            c = self.encrypt(m, public_key) 
            encrypted.append(c) 
        return encrypted 

    def decrypt_string(self, encrypted, private_key): 
        """ 
        Decrypt a list of encrypted values back to string 
        """ 
        decrypted = [] 
        for c in encrypted: 
            m = self.decrypt(c, private_key) 
            decrypted.append(chr(m)) 
        return ''.join(decrypted) 


# Demonstration and Examples 
def demonstrate_rsa(): 
    """ 
    Comprehensive RSA demonstration 
    """ 
    rsa = RSA() 
    # Generate keys with small primes for demonstration 
    public_key, private_key = rsa.generate_keypair(bits=16) 
    print("\n" + "="*60) 
    print("ENCRYPTION DEMONSTRATION") 
    print("="*60) 
    # Test with single number 
    message = 12345 
    print(f"\nOriginal Message (numeric): {message}") 
    ciphertext = rsa.encrypt(message, public_key) 
    print(f"Encrypted Ciphertext: {ciphertext}") 
    decrypted = rsa.decrypt(ciphertext, private_key) 
    print(f"Decrypted Message: {decrypted}") 
    if message == decrypted: 
        print("✓ Encryption/Decryption successful!") 
    # Test with string (if n is large enough) 
    print("\n" + "="*60) 
    print("STRING ENCRYPTION DEMONSTRATION") 
    print("="*60) 
    try: 
        text = "HELLO" 
        print(f"\nOriginal Text: '{text}'") 
        encrypted_text = rsa.encrypt_string(text, public_key) 
        print(f"Encrypted (list of numbers): {encrypted_text}")
        decrypted_text = rsa.decrypt_string(encrypted_text, private_key) 
        print(f"Decrypted Text: '{decrypted_text}'") 
        if text == decrypted_text: 
            print("String encryption/decryption successful!") 
    except ValueError as e: 
        print(f"Note: {e}") 
        print("(Use larger primes for encrypting text)") 


# Run demonstration 
if __name__ == "__main__": 
    demonstrate_rsa()
    # Additional manual example with known small primes 
    print("\n" + "="*60) 
    print("MANUAL EXAMPLE WITH SMALL PRIMES") 
    print("="*60) 
    rsa = RSA() 
    # Use the example from lecture notes 
    p, q = 61, 53 
    n = p * q 
    phi = (p - 1) * (q - 1) 
    e = 17 
    d = rsa.mod_inverse(e, phi) 
    public_key = (n, e) 
    private_key = (n, d) 
    print("\nManual Setup:") 
    print(f"  p = {p}, q = {q}") 
    print(f"  n = {n}") 
    print(f"  φ(n) = {phi}") 
    print(f"  e = {e}") 
    print(f"  d = {d}") 
    # Encrypt and decrypt 
    message = 123 
    print(f"\nEncrypting message: {message}") 
    ciphertext = rsa.encrypt(message, public_key) 
    print(f"  Ciphertext: {ciphertext}") 
decrypted = rsa.decrypt(ciphertext, private_key) 
print(f"  Decrypted: {decrypted}") 
print(f"  Match: {message == decrypted} ✓")