import random

# Extended Euclidean Algorithm for modular inverse
def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return g, x, y

def mod_inverse(a, p):
    a %= p
    g, x, y = extended_gcd(a, p)
    if g != 1:
        raise ValueError("No inverse exists!")
    return x % p

# ElGamal Key Generation
def mod_exp(base, exponent, modulus): # From question 1 file
    result = 1
    base %= modulus
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulus
        base = (base * base) % modulus
        exponent //= 2
    return result

def elgamal_keygen(p, g):
    private = random.randint(2, p - 2)
    h = mod_exp(g, private, p)
    return (p, g, h), private

def elgamal_encrypt_with_fixed_k(m, p, g, h, k):
    if not (0 <= m < p):
        raise ValueError("Message out of range 0 <= m < p")
    c1 = mod_exp(g, k, p)        # g^k mod p
    s  = mod_exp(h, k, p)        # h^k mod p
    c2 = (m * s) % p
    return c1, c2


def attack_reused_k(c1_1, c2_1, c1_2, c2_2, known_m1, p):
    print("--- ElGamal Reused k Attack ---")

    # 1. checking for reused k (C1 values must match)
    if c1_1 == c1_2:
        print("Detected : C1 values are identical !")
        print("k was reused.")
    else:
        print("C1 values are different. No reused k detected.")
        return None

    print()
    print(f"Message 1: {known_m1}")
    print("Message 2: [unknown]")
    print()
    print(f"Ciphertext 1: ({c1_1}, {c2_1})")
    print(f"Ciphertext 2: ({c1_2}, {c2_2})")
    print()

    # 2. Computing ratio = C2_1 / C2_2 mod p
    ratio = (c2_1 * mod_inverse(c2_2, p)) % p
    print(f"Ratio C2/C2': {ratio}")

    # 3. Recovering m2 by using:
    #    ratio = m1 / m2  =>  m2 = m1 * (ratio^(-1)) mod p
    ratio_inv = mod_inverse(ratio, p)
    recovered_m2 = (known_m1 * ratio_inv) % p

    print(f"Recovered Message 2 (from known Message 1) : {recovered_m2}")
    print("Attack successful !")

    return recovered_m2


if __name__ == "__main__":
    p = 31847
    g = 5
    # Key generation
    public_key, private_key = elgamal_keygen(p, g)
    _, _, h = public_key

    # Choose two messages (integers)
    # m1 is known to attacker, m2 is unknown
    m1 = ord('A')         # 65, known plaintext
    m2 = ord('Z')         # 90, "secret" plaintext

    # same k for both encryptions
    k_fixed = random.randint(2, p - 2)

    c1_1, c2_1 = elgamal_encrypt_with_fixed_k(m1, p, g, h, k_fixed)
    c1_2, c2_2 = elgamal_encrypt_with_fixed_k(m2, p, g, h, k_fixed)

    recovered_m2 = attack_reused_k(c1_1, c2_1, c1_2, c2_2, m1, p)

    # Verification:
    print("\n[Verification]")
    print(f"Actual Message 2       : {m2}")
    print(f"Recovered Message 2    : {recovered_m2}")
    print(f"Correct recovery? {m2 == recovered_m2}")
