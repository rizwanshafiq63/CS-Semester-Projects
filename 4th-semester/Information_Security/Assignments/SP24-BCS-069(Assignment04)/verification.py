import sys
import hashlib
import math


def computeInverse(in1, in2):
    """
    Computes multiplicative inverse using Extended Euclidean Algorithm.
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
    Computes SHA-1 hash of file and returns integer value.
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


def verification():
    """
    Verifies DSA signature stored in signature.txt for a given file.
    """
    if len(sys.argv) < 2:
        print("Format: python verification.py filename")
    elif len(sys.argv) == 2:
        print("Checking the signature...")
        fileName = sys.argv[1]

        with open("key.txt", "r") as file1:
            p = int(file1.readline().rstrip())
            q = int(file1.readline().rstrip())
            g = int(file1.readline().rstrip())
            h = int(file1.readline().rstrip())

        with open("signature.txt", "r") as file2:
            c1 = int(file2.readline().rstrip())
            c2 = int(file2.readline().rstrip())

        t1 = shaHash(fileName)

        inverseC2 = computeInverse(c2, q)

        t1 = (t1 * inverseC2) % q

        t2 = computeInverse(c2, q)
        t2 = (t2 * c1) % q

        valid1 = squareAndMultiply(g, t1, p)
        valid2 = squareAndMultiply(h, t2, p)
        valid = ((valid1 * valid2) % p) % q

        if valid == c1:
            print("Valid signature")
        else:
            print("Invalid signature")


if __name__ == "__main__":
    verification()
