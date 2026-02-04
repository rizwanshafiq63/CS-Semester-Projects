import random
from math import gcd
from miller import generateLargePrime


def mod_inverse(a, m):
    t, new_t = 0, 1
    r, new_r = m, a
    while new_r != 0:
        q = r // new_r
        t, new_t = new_t, t - q * new_t
        r, new_r = new_r, r - q * new_r
    if r > 1:
        raise ValueError("no inverse")
    if t < 0:
        t += m
    return t


def generate_rsa_keys(keysize=1024):
    print("generating rsa key pair...")

    half_bits = keysize // 2
    p = generateLargePrime(half_bits)
    q = generateLargePrime(half_bits)

    while q == p:
        q = generateLargePrime(half_bits)

    n = p * q
    phi = (p - 1) * (q - 1)

    e = 65537
    if gcd(e, phi) != 1:
        while True:
            e = random.randrange(3, phi - 1, 2)
            if gcd(e, phi) == 1:
                break

    d = mod_inverse(e, phi)

    print("done, n has", n.bit_length(), "bits")
    return (e, n), (d, n)


def rsa_encrypt(message, public_key):
    e, n = public_key
    m_int = int.from_bytes(message.encode("utf-8"), "big")
    if m_int >= n:
        raise ValueError("message too large for modulus")
    return pow(m_int, e, n)


def rsa_decrypt(ciphertext, private_key):
    d, n = private_key
    m_int = pow(ciphertext, d, n)
    m_bytes = m_int.to_bytes((m_int.bit_length() + 7) // 8, "big")
    return m_bytes.decode("utf-8")


def main():
    pub, priv = generate_rsa_keys(1024)

    messages = [
        "Hello RSA from BCS4B!",
        "Public Key Cryptography Lab Assignment",
        "This is the third test message 12345 :)"
    ]

    print("\n=== RSA Encryption/Decryption Tests ===\n")

    for i, msg in enumerate(messages, start=1):
        print("Test #", i)
        print("original:", msg)

        c = rsa_encrypt(msg, pub)
        print("ciphertext:", c)

        back = rsa_decrypt(c, priv)
        print("decrypted:", back)

        if back == msg:
            print("result: OK\n")
        else:
            print("result: MISMATCH\n")


if __name__ == "__main__":
    main()
