# from miller import *
from miller import isPrime, generateLargePrime, rabinMiller
from math import gcd
import random


def squareAndMultiply(x, c, n):
    """
    Efficient modular exponentiation using square-and-multiply algorithm.
    Computes x^c mod n.

    Args:
        x: Base
        c: Exponent
        n: Modulus
    Returns:
        Result of x^c mod n
    """
    z = 1
    # Convert exponent to binary (reversed)
    c_bits = f"{c:b}"[::-1]
    l = len(c_bits)

    # Process each bit from most significant to least significant
    for i in range(l - 1, -1, -1):
        z = pow(z, 2, n)
        if c_bits[i] == '1':
            z = (z * x) % n
    return z


def keyGeneration():
    """
    Generates DSA key pair and global parameters.

    Generates:
        - Global parameters: p, q, g
        - Public key: h (or y)
        - Private key: a (or x)

    Saves keys to files:
        - key.txt: Contains p, q, g, h (public parameters)
        - secretkey.txt: Contains a (private key)
    """
    print("Computing key values, please wait...")

    loop = True
    while loop:
        # Generate q: 160-bit prime
        q = generateLargePrime(160)

        # Generate k: 416-bit random number
        k = random.randrange(2 ** 415, 2 ** 416)

        # Calculate p = kq + 1
        p = (k * q) + 1

        # Ensure p is prime
        while not isPrime(p):
            k = random.randrange(2 ** 415, 2 ** 416)
            q = generateLargePrime(160)
            p = (k * q) + 1

        # Get bit length of p
        L = p.bit_length()

        # Find generator g
        # g = t^((p-1)/q) mod p
        # Must satisfy: g^q mod p = 1
        t = random.randint(1, p - 1)
        g = squareAndMultiply(t, (p - 1) // q, p)

        # Verify all DSA parameter constraints
        if (L >= 512 and L <= 1024 and L % 64 == 0 and
                gcd(p - 1, q) > 1 and
                squareAndMultiply(g, q, p) == 1):
            loop = False

    # Generate private key: a (random integer in range [2, q-1])
    a = random.randint(2, q - 1)

    # Generate public key: h = g^a mod p
    h = squareAndMultiply(g, a, p)

    # Save public parameters to key.txt
    with open("key.txt", "w") as file1:
        file1.write(str(p) + "\n")
        file1.write(str(q) + "\n")
        file1.write(str(g) + "\n")
        file1.write(str(h))

    # Save private key to secretkey.txt
    with open("secretkey.txt", "w") as file2:
        file2.write(str(a))

    print("Verification key stored at key.txt")
    print("Secret key stored at secretkey.txt")


# Run key generation when the script is executed directly
if __name__ == "__main__":
    keyGeneration()
