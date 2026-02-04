from miller import isPrime, generateLargePrime, rabinMiller
from math import gcd
import random


def squareAndMultiply(x, c, n):
    z = 1
    c_bits = f"{c:b}"[::-1]
    l = len(c_bits)

    for i in range(l - 1, -1, -1):
        z = pow(z, 2, n)
        if c_bits[i] == '1':
            z = (z * x) % n
    return z


def keyGeneration():
    """
    Generates DSA key pair and global parameters.
    Saves:
        - key.txt: p, q, g, h (public parameters)
        - secretkey.txt: a (private key)
    """
    print("Computing key values, please wait...")

    loop = True
    while loop:
        q = generateLargePrime(160)
        k = random.randrange(2 ** 415, 2 ** 416)
        p = (k * q) + 1

        while not isPrime(p):
            k = random.randrange(2 ** 415, 2 ** 416)
            q = generateLargePrime(160)
            p = (k * q) + 1

        L = p.bit_length()

        # Compute generator g
        t = random.randint(1, p - 1)
        g = squareAndMultiply(t, (p - 1) // q, p)

        if (512 <= L <= 1024 and L % 64 == 0 and
                gcd(p - 1, q) > 1 and
                squareAndMultiply(g, q, p) == 1):
            loop = False

    a = random.randint(2, q - 1)
    h = squareAndMultiply(g, a, p)

    with open("key.txt", "w") as file1:
        file1.write(str(p) + "\n")
        file1.write(str(q) + "\n")
        file1.write(str(g) + "\n")
        file1.write(str(h))

    with open("secretkey.txt", "w") as file2:
        file2.write(str(a))

    print("Verification key stored at key.txt")
    print("Secret key stored at secretkey.txt")


if __name__ == "__main__":
    keyGeneration()
