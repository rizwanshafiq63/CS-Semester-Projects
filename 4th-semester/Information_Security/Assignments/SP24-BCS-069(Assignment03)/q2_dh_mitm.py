import random

def mod_exp(base, exponent, modulus):
    # From question 1 file
    result = 1
    base %= modulus

    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulus

        base = (base * base) % modulus
        exponent //= 2

    return result


def mitm_attack(p, g):
    a = random.randint(2, p - 2)    # Alice's private key
    b = random.randint(2, p - 2)    # Bob's private key
    A = mod_exp(g, a, p)            # Alice's public key
    B = mod_exp(g, b, p)            # Bob's public key

    # Eve chooses two separate private keys
    e1 = random.randint(2, p - 2)
    e2 = random.randint(2, p - 2)

    # Eve's fake public keys
    E1 = mod_exp(g, e1, p)      # sent to Alice
    E2 = mod_exp(g, e2, p)      # sent to Bob

    # Alice receives E1
    K_A = mod_exp(E1, a, p)     # Alice's computed DH key (with Eve)

    # Bob receives E2
    K_B = mod_exp(E2, b, p)     # Bob's computed DH key (with Eve)

    # Eve knows both shared keys:
    K_EA = mod_exp(A, e1, p)    # shared key with Alice
    K_EB = mod_exp(B, e2, p)    # shared key with Bob

    # Print required output
    print("Alice's computed key :", K_A)
    print("Bob's computed key   :", K_B)
    print("Eve's key with Alice :", K_EA)
    print("Eve's key with Bob   :", K_EB)
    print("Attack successful : Alice and Bob have different keys!")


if __name__ == "__main__":
    p = 467
    g = 2
    mitm_attack(p, g)
