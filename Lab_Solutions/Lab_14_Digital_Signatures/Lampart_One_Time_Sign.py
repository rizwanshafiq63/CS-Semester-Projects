import hashlib
import secrets

# ==================== KEY GENERATION ====================

def keygen():
    """
    Generates a Lamport key pair (private key and public key).

    Returns:
        keypair: [private_key, public_key]
            - private_key: 2D list [2][255] of 255-bit random numbers (as bit strings)
            - public_key: 2D list [2][255] of SHA-256 hashes (as hex strings)
    """
    # Initialize private key structure: 2 lists of 255 elements each
    skey = [[0] * 255, [1] * 255]

    # Generate random numbers for private key
    for i in range(len(skey)):             # For both lists (0 and 1)
        for j in range(len(skey[i])):      # For each position
            # Generate 255-bit random number
            skey[i][j] = bin(secrets.randbits(255))[2:]
            # Pad with zeros to ensure 255 bits
            skey[i][j] = '0' * (255 - len(skey[i][j])) + skey[i][j]

    # Initialize public key structure
    pkey = [[0] * 255, [1] * 255]

    # Generate public key by hashing private key elements
    for i in range(len(pkey)):
        for j in range(len(pkey[i])):
            # Hash each private key element and store as a hex string
            pkey[i][j] = hashlib.sha256(skey[i][j].encode()).hexdigest()

    keypair = [skey, pkey]
    return keypair


# ==================== SIGNATURE GENERATION ====================

def signgen(message, skey):
    """
    Generates a Lamport signature for the given message.

    Args:
        message: String message to sign
        skey: Private key (from keygen)

    Returns:
        signature: List of 255 numbers from private key
    """
    # Hash the message to get 256-bit digest
    mhash = int(hashlib.sha256(message.encode()).hexdigest(), 16)

    # Initialize signature list
    signature = [0] * 255

    # For each bit position in the hash
    for i in range(255):
        # Extract the i-th bit using bit shifting and masking
        k = (mhash >> i) & 1   # k is either 0 or 1
        # Select the corresponding number from the private key
        signature[i] = skey[k][i]

    return signature


# ==================== SIGNATURE VERIFICATION ====================

def verification(message, pkey, signature):
    """
    Verifies a Lamport signature against the message and public key.

    Args:
        message: Original message
        pkey: Public key (from keygen)
        signature: Signature to verify (from signgen)

    Returns:
        True if the signature is valid, False otherwise
    """
    # Hash the message to get 256-bit digest
    mhash = int(hashlib.sha256(message.encode()).hexdigest(), 16)

    # Verify each component of the signature
    for i in range(255):
        # Extract the i-th bit
        k = (mhash >> i) & 1   # k is either 0 or 1

        # Hash the signature component
        verify = hashlib.sha256(signature[i].encode()).hexdigest()

        # Compare with corresponding public key element
        if pkey[k][i] != verify:
            return False    # Signature invalid

    return True             # All components matched, signature valid


# ==================== EXAMPLE USAGE ====================

if __name__ == "__main__":
    # Generate key pair
    keypair = keygen()

    # Message to sign
    message = "I am god."

    # Generate signature
    signature = signgen(message, keypair[0])

    # Verify signature
    print("Signature valid:", verification(message, keypair[1], signature))
