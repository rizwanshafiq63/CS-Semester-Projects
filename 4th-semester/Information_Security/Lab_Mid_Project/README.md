# Secure Complaint / Whistleblower System 

This system allows authenticated users to securely submit complaints that are encrypted using AES and stored in an immutable blockchain. An admin can later review complaints after decryption.

---

## 🔐 Security Features

| Feature     | Technique Used |
|-------------|----------------|
| Confidentiality | AES-256 (CBC Mode + IV + PKCS#7 Padding) |
| Integrity       | SHA-256 Hash of Ciphertext (`data_hash`) |
| Immutability    | Blockchain with Proof-of-Work mining |
| Authentication  | SHA-256 password hashing |
| Anonymity       | Masked user IDs + uid_hash on chain |

---

## ⚙️ Setup & Run

```bash
pip install pycryptodome
python Secure_Complaint_System.py
