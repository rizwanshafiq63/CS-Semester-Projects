import random

def mod_exp(base, exponent, modulus):
    result = 1
    base = base % modulus

    while exponent > 0:
        # If current bit of exponent is 1, multiply result by base
        if exponent % 2 == 1:
            result = (result * base) % modulus

        # Move to next bit: square the base, shift exponent right
        base = (base * base) % modulus
        exponent //= 2

    return result

def diffie_hellman(p, g):

    # 1. Choose private keys
    # we select random integers in the range [2, p-2] because 
    # lower values like 0 or 1 will make the key exchange  insecure and
    # upper limit p-2 ensures that private key is less than p-1
    a = random.randint(2, p - 2)    # Alice's private key
    b = random.randint(2, p - 2)    # Bob's private key

    # 2. Computing public keys
    A = mod_exp(g, a, p)            # Alice's public key
    B = mod_exp(g, b, p)            # Bob's public key

    # 3. Compute shared keys on both sides
    K_A = mod_exp(B, a, p)          # Alice's shared key
    K_B = mod_exp(A, b, p)          # Bob's shared key

    # 4. output
    print("Alice's private key :", a)
    print("Alice's public key  :", A)
    print("Bob's private key   :", b)
    print("Bob's public key    :", B)
    print("Alice's computed shared key :", K_A)
    print("Bob's computed shared key   :", K_B)
    print("Keys match :", K_A == K_B)

    return a, A, b, B, K_A, K_B


if __name__ == "__main__":
    prime = 467
    generator = 2 
    diffie_hellman(prime, generator)
