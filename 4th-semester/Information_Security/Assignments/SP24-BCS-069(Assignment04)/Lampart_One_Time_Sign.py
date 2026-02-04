import hashlib
import secrets


def keygen():
    """
    Generates a Lamport key pair (private key and public key).
    """
    skey = [[0] * 255, [1] * 255]

    for i in range(len(skey)):
        for j in range(len(skey[i])):
            skey[i][j] = bin(secrets.randbits(255))[2:]
            skey[i][j] = '0' * (255 - len(skey[i][j])) + skey[i][j]

    pkey = [[0] * 255, [1] * 255]

    for i in range(len(pkey)):
        for j in range(len(pkey[i])):
            pkey[i][j] = hashlib.sha256(skey[i][j].encode()).hexdigest()

    return [skey, pkey]


def signgen(message, skey):
    """
    Generates a Lamport signature for the given message.
    """
    mhash = int(hashlib.sha256(message.encode()).hexdigest(), 16)
    signature = [0] * 255

    for i in range(255):
        k = (mhash >> i) & 1
        signature[i] = skey[k][i]

    return signature


def verification(message, pkey, signature):
    """
    Verifies a Lamport signature.
    """
    mhash = int(hashlib.sha256(message.encode()).hexdigest(), 16)

    for i in range(255):
        k = (mhash >> i) & 1
        verify = hashlib.sha256(signature[i].encode()).hexdigest()

        if pkey[k][i] != verify:
            return False

    return True


if __name__ == "__main__":
    keypair = keygen()
    message = "I am god."
    signature = signgen(message, keypair[0])
    print("Signature valid:", verification(message, keypair[1], signature))
