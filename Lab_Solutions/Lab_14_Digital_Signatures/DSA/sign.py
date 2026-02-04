# from miller import *
from miller import isPrime, generateLargePrime, rabinMiller
import sys
import hashlib
import math
import random


def computeInverse(in1, in2):
    """
    Computes the multiplicative inverse of in1 modulo in2.
    Uses Extended Euclidean Algorithm.

    Args:
        in1: Number to find inverse of
        in2: Modulus
    Returns:
        Multiplicative inverse of in1 mod in2
    """
    aL = [in1]
    bL = [in2]
    tL = [0]
    t = 1
    sL = [1]
    s = 0

    q = math.floor(aL[0] / bL[0])
    r = aL[0] - (q * bL[0])

    while r > 0:
        temp = tL[0] - (q * t)
        tL[0] = t
        t = temp

        temp = sL[0] - (q * s)
        sL[0] = s
        s = temp

        aL[0] = bL[0]
        bL[0] = r

        q = math.floor(aL[0] / bL[0])
        r = aL[0] - (q * bL[0])

    r = bL[0]
    inverse = s % in2
    return inverse


def squareAndMultiply(x, c, n):
    """
    Efficient modular exponentiation.
    """
    z = 1
    c_bits = f"{c:b}"[::-1]
    l = len(c_bits)

    for i in range(l - 1, -1, -1):
        z = pow(z, 2, n)
        if c_bits[i] == '1':
            z = (z * x) % n
    return z


def shaHash(fileName):
    """
    Computes SHA-1 hash of a file.

    Args:
        fileName: Path to file
    Returns:
        Integer value of hash
    """
    BLOCKSIZE = 65536
    hasher = hashlib.sha1()

    with open(fileName, 'rb') as afile:
        buf = afile.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(BLOCKSIZE)

    hex_digest = "0x" + hasher.hexdigest()
    return int(hex_digest, 0)


def sign():
    """
    Signs a file using DSA.

    Usage: python sign.py filename

    Generates signature (c1, c2) where:
        c1 = r = (g^k mod p) mod q
        c2 = s = k^(-1)[H(M) + a*r] mod q
    """
    if len(sys.argv) < 2:
        print("Format: python sign.py filename")
    elif len(sys.argv) == 2:
        print("Signing the file...")
        fileName = sys.argv[1]

        # Read public parameters
        with open("key.txt", "r") as file1:
            p = int(file1.readline().rstrip())
            q = int(file1.readline().rstrip())
            g = int(file1.readline().rstrip())
            h = int(file1.readline().rstrip())

        # Read private key
        with open("secretkey.txt", "r") as file2:
            a = int(file2.readline().rstrip())

        loop = True
        while loop:
            # Generate random k in range [1, q-1]
            r = random.randint(1, q - 1)

            # Compute c1 = r = (g^k mod p) mod q
            c1 = squareAndMultiply(g, r, p)
            c1 = c1 % q

            # Compute c2 = s = k^(-1)[H(M) + a*r] mod q
            c2 = shaHash(fileName) + (a * c1)
            Rinverse = computeInverse(r, q)
            c2 = (c2 * Rinverse) % q

            # Ensure r and s are not zero
            if c1 != 0 and c2 != 0:
                loop = False

        # Save signature to file
        with open("signature.txt", "w") as sigfile:
            sigfile.write(str(c1) + "\n")
            sigfile.write(str(c2))

        print("Signature stored at signature.txt")


# Run signing
if __name__ == "__main__":
    sign()
