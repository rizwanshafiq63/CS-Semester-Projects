# REPORT — Secure Complaint / Whistleblower System

## Objective
This project implements a secure Complaint/Whistleblower System using cryptographic techniques and blockchain to ensure privacy, integrity, and immutability of user-submitted complaints.

---

## Labs Mapping

| Lab | Concept Used in Project |
|-----|-------------------------|
| **Lab 01–02** | User management using Python dictionaries, SHA-256 password hashing, one-complaint-per-user, and input validation. |
| **Lab 04** | AES-CBC encryption using PyCryptodome with PKCS#7 padding and IV for confidentiality of complaints. |
| **Lab 06** | Data integrity using `data_hash = SHA-256(ciphertext)`, verified before decryption. |
| **Lab 07** | Blockchain implementation with Proof-of-Work mining, chained blocks, `prev_hash`, nonce, and validation via `is_valid()`.|

---

## System Security Design

- **AES Encryption (Confidentiality):**  
  All complaints are encrypted using AES-CBC. A fixed master key is defined in the code, converted through a KDF (SHA-256) into a 256-bit AES key.

- **Hashing (Integrity & Authentication):**
  - Passwords are never stored—only `hash_password()` values.
  - Ea
