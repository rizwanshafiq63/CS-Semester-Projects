# Task5_Integrated_Secure_Communication.py

from pathlib import Path
import sys

# RSA (Task 1)
from Task_01_RSA_Implementation import generate_rsa_keys, rsa_encrypt, rsa_decrypt

# Mock CA (Task 2)
from Task_02_Mock_CA import MockCA

# DSA modules (Task 3)
import keygen
import sign as dsa_sign
import verification as dsa_verify

# Lamport OTS (Task 4)
from Lampart_One_Time_Sign import keygen as ots_keygen
from Lampart_One_Time_Sign import signgen as ots_sign
from Lampart_One_Time_Sign import verification as ots_verify


def dsa_sign_file(filename: str) -> None:
    """Run DSA signing as if: python sign.py <filename>."""
    old_argv = sys.argv[:]
    sys.argv = ["sign.py", filename]
    try:
        dsa_sign.sign()
    finally:
        sys.argv = old_argv


def dsa_verify_file(filename: str) -> None:
    """Run DSA verification as if: python verification.py <filename>."""
    old_argv = sys.argv[:]
    sys.argv = ["verification.py", filename]
    try:
        dsa_verify.verification()
    finally:
        sys.argv = old_argv


def setup_keys_and_ca():
    print("=== SETUP PHASE ===\n")

    # RSA keys for Alice and Bob
    print("[1] Generating RSA keys for Alice and Bob...")
    alice_rsa_public, alice_rsa_private = generate_rsa_keys(1024)
    bob_rsa_public, bob_rsa_private = generate_rsa_keys(1024)
    print("    -> RSA keys generated for both.\n")

    # Root CA and certificates
    print("[2] Creating Mock CA and issuing certificates for Alice & Bob...")
    ca = MockCA()
    ca.create_root_ca()
    alice_priv_cert_key, alice_cert = ca.issue_certificate(
        common_name="Alice", organization="CS Department"
    )
    bob_priv_cert_key, bob_cert = ca.issue_certificate(
        common_name="Bob", organization="CS Department"
    )
    print("    -> Certificates issued.\n")

    # DSA parameters and key files for Alice (key.txt / secretkey.txt)
    print("[3] Generating DSA parameters and keys for Alice...")
    keygen.keyGeneration()
    print("    -> DSA key files created.\n")

    # Lamport OTS keys for Alice
    print("[4] Generating Lamport OTS key pair for Alice...")
    ots_skey, ots_pkey = ots_keygen()
    print("    -> Lamport private and public keys generated.\n")

    data = {
        "alice_rsa_public": alice_rsa_public,
        "alice_rsa_private": alice_rsa_private,
        "bob_rsa_public": bob_rsa_public,
        "bob_rsa_private": bob_rsa_private,
        "ca": ca,
        "alice_cert": alice_cert,
        "bob_cert": bob_cert,
        "ots_skey": ots_skey,
        "ots_pkey": ots_pkey,
    }

    return data


def scenario_success(context):
    print("\n=== SCENARIO 1: SUCCESSFUL COMMUNICATION ===\n")

    alice_pub = context["alice_rsa_public"]
    alice_priv = context["alice_rsa_private"]
    bob_pub = context["bob_rsa_public"]
    bob_priv = context["bob_rsa_private"]
    ca = context["ca"]
    alice_cert = context["alice_cert"]
    ots_skey = context["ots_skey"]
    ots_pkey = context["ots_pkey"]

    # Alice's original message
    M = "Hello Bob, this is Alice. Meet me at 10:00 AM."
    print(f"[1] Alice's original message M:\n    {M}\n")

    # Save message to file for DSA
    msg_file = Path("task5_message.txt")
    msg_file.write_text(M, encoding="utf-8")

    # Encrypt with Bob's RSA public key
    print("[2] Alice encrypts M with Bob's RSA public key...")
    C = rsa_encrypt(M, bob_pub)
    print(f"    Ciphertext C (integer): {C}\n")

    # DSA signature on the message file
    print("[3] Alice signs M using DSA...")
    dsa_sign_file(str(msg_file))
    print("    -> DSA signature stored in signature.txt\n")

    # Lamport OTS signature
    print("[4] Alice signs M using Lamport OTS...")
    ots_signature = ots_sign(M, ots_skey)
    print("    -> Lamport OTS signature generated.\n")

    print("[5] Alice sends (C, DSA signature, OTS signature, Alice's certificate).\n")

    # --- Bob's side ---

    print("=== Bob's processing of received data ===\n")

    # Certificate validation
    print("[5a] Verifying Alice's certificate with CA...")
    if ca.verify_certificate(alice_cert):
        print("    -> Alice's certificate is VALID and NOT revoked.\n")
    else:
        print("    -> Alice's certificate is INVALID. Abort.\n")
        return

    # DSA verification
    print("[5b] Verifying DSA signature on M (should be VALID)...")
    dsa_verify_file(str(msg_file))
    print()

    # OTS verification
    print("[5c] Verifying Lamport OTS signature on M (should be VALID)...")
    if ots_verify(M, ots_pkey, ots_signature):
        print("    -> Lamport OTS signature is VALID.\n")
    else:
        print("    -> Lamport OTS signature is INVALID.\n")

    # Decrypt ciphertext
    print("[5d] Bob decrypts C with his RSA private key...")
    recovered_M = rsa_decrypt(C, bob_priv)
    print(f"    Decrypted message M':\n    {recovered_M}\n")

    if recovered_M == M:
        print("Result: Communication SUCCESSFUL (private, authenticated, integral).\n")
    else:
        print("Result: Decryption mismatch (something went wrong).\n")

    return M, C, ots_signature


def scenario_tampering(context, original_message, ciphertext, ots_signature):
    print("\n=== SCENARIO 2: MESSAGE TAMPERING DETECTION ===\n")

    ca = context["ca"]
    alice_cert = context["alice_cert"]
    ots_pkey = context["ots_pkey"]

    # Certificate still valid
    print("[1] Verifying Alice's certificate again (should still be VALID)...")
    ca.verify_certificate(alice_cert)
    print()

    # Overwrite message file with a tampered message
    tampered_message = "HELLO BOB, THIS MESSAGE WAS TAMPERED!"
    Path("task5_message.txt").write_text(tampered_message, encoding="utf-8")
    print("[2] Attacker modifies the message file after it was signed:")
    print(f"    Tampered message:\n    {tampered_message}\n")

    # DSA verification should now fail
    print("[3] Verifying DSA signature on TAMPERED message (should be INVALID)...")
    dsa_verify_file("task5_message.txt")
    print()

    # OTS verification should also fail
    print("[4] Verifying Lamport OTS signature on TAMPERED message (should be INVALID)...")
    if ots_verify(tampered_message, ots_pkey, ots_signature):
        print("    -> OTS verification unexpectedly SUCCEEDED (check logic).")
    else:
        print("    -> OTS verification FAILED as expected. Tampering detected.\n")

    print("Result: Any change in the message breaks both DSA and OTS signatures.\n")


def scenario_revocation(context):
    print("\n=== SCENARIO 3: CERTIFICATE REVOCATION ===\n")

    ca = context["ca"]
    alice_cert = context["alice_cert"]

    # CA revokes Alice's certificate
    print("[1] CA revokes Alice's certificate...")
    ca.revoke_certificate(alice_cert.serial_number)
    ca.build_crl()
    print("    -> Alice's certificate serial added to CRL.\n")

    # Bob checks the certificate again
    print("[2] Bob validates Alice's certificate AFTER revocation (should be INVALID)...")
    if ca.verify_certificate(alice_cert):
        print("    -> Unexpected: certificate still considered valid.")
    else:
        print("    -> Correct: certificate is now INVALID / REVOKED.\n")

    print("Result: Even with correct signatures, a revoked certificate must NOT be trusted.\n")


def main():
    context = setup_keys_and_ca()

    M, C, ots_sig = scenario_success(context)

    scenario_tampering(context, M, C, ots_sig)

    scenario_revocation(context)

    print("=== END OF TASK 5 DEMO ===")


if __name__ == "__main__":
    main()
