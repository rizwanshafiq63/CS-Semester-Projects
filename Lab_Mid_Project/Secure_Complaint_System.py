"""
================================================================
            Secure Complaint / Whistleblower System              
================================================================
"""

import time
import json
import hashlib
from dataclasses import dataclass, asdict
from typing import Tuple

# ========================= Config =========================
MASTER_KEY = "MyStrongMasterKey!2025"     
ADMIN_DEFAULT_PASSWORD = "admin123"
POW_DIFFICULTY = 2
EXPORT_FILENAME = "blockchain_export.json"

# ====================== Hash helpers ======================
def sha256_hex(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def hash_text(s: str) -> str:
    return sha256_hex(s.encode())

def hash_password(pw: str) -> str:
    return sha256_hex(pw.encode())

def mask_user_id(uid: str) -> str:
    return uid[:2] + "*"*(max(0, len(uid) - 4)) + uid[-2:] if len(uid) > 4 else "****"

# ==================== AES (PyCryptodome) ==================
try:
    from Crypto.Cipher import AES
    from Crypto.Random import get_random_bytes
except Exception:
    AES = None
    get_random_bytes = None

def kdf_key(master_key_str: str) -> bytes:
    # Derive 32-byte AES-256 key from master key string.
    return hashlib.sha256(master_key_str.encode()).digest()

def pkcs7_pad(data: bytes, block_size: int = 16) -> bytes:
    pad_len = block_size - (len(data) % block_size)
    if pad_len == 0:
        pad_len = block_size
    return data + bytes([pad_len]) * pad_len

def pkcs7_unpad(data: bytes, block_size: int = 16) -> bytes:
    if not data or len(data) % block_size != 0:
        raise ValueError("Invalid padded data length")
    pad_len = data[-1]
    if pad_len < 1 or pad_len > block_size:
        raise ValueError("Invalid padding")
    if data[-pad_len:] != bytes([pad_len]) * pad_len:
        raise ValueError("Bad padding bytes")
    return data[:-pad_len]

def aes_encrypt_pt(plaintext: str, key_bytes: bytes) -> Tuple[bytes, bytes]:
    iv = get_random_bytes(16)
    cipher = AES.new(key_bytes, AES.MODE_CBC, iv)
    ct = cipher.encrypt(pkcs7_pad(plaintext.encode(), 16))
    return iv, ct

def aes_decrypt_ct(iv: bytes, ciphertext: bytes, key_bytes: bytes) -> str:
    cipher = AES.new(key_bytes, AES.MODE_CBC, iv)
    pt = pkcs7_unpad(cipher.decrypt(ciphertext), 16)
    return pt.decode()

# ======================= Blockchain =======================
@dataclass
class Block:
    index: int
    timestamp: float
    user_mask: str
    uid_hash: str            # sha256(uid) 
    key_hash: str            # sha256(master_key_str) — binds to correct key
    iv_hex: str              # AES IV (hex)
    enc_hex: str             # ciphertext (hex)
    data_hash: str           # sha256(ciphertext bytes)
    prev_hash: str
    nonce: int = 0
    hash: str = ""

    def compute_hash(self) -> str:
        s = (
            f"{self.index}{self.timestamp}{self.user_mask}{self.uid_hash}"
            f"{self.key_hash}{self.iv_hex}{self.enc_hex}{self.data_hash}"
            f"{self.prev_hash}{self.nonce}"
        )
        return sha256_hex(s.encode())

    def mine(self, difficulty: int):
        prefix = "0" * difficulty
        while True:
            self.hash = self.compute_hash()
            if self.hash.startswith(prefix):
                return
            self.nonce += 1

class Blockchain:
    def __init__(self, difficulty: int = 2):
        self.difficulty = difficulty
        g = Block(
            index=0,
            timestamp=time.time(),
            user_mask="GENESIS",
            uid_hash="",
            key_hash="",
            iv_hex="",
            enc_hex="",
            data_hash="",
            prev_hash="0" * 64
        )
        g.hash = g.compute_hash()
        self.chain = [g]

    def add_block(self, **fields):
        last = self.chain[-1]
        b = Block(index=len(self.chain), timestamp=time.time(), prev_hash=last.hash, **fields)
        b.mine(self.difficulty)
        self.chain.append(b)
        return b

    def is_valid(self) -> bool:
        for i in range(1, len(self.chain)):
            cur = self.chain[i]
            prev = self.chain[i - 1]
            if cur.prev_hash != prev.hash:
                return False
            if cur.compute_hash() != cur.hash:
                return False
        return True

# ====================== Application =======================
class ComplaintApp:
    def __init__(self, master_key_str: str, admin_password: str = ADMIN_DEFAULT_PASSWORD, difficulty: int = POW_DIFFICULTY):
        if AES is None:
            raise RuntimeError("PyCryptodome not available. Install with: pip install pycryptodome")

        self.master_key_str = master_key_str
        self.master_key_hash = hash_text(master_key_str)
        self.master_key_bytes = kdf_key(master_key_str)

        self.users = {}
        self.admin_pw_hash = hash_password(admin_password)
        self.bc = Blockchain(difficulty=difficulty)

    def set_admin_password(self, old_pw: str, new_pw: str):
        if self.admin_pw_hash != hash_password(old_pw):
            raise PermissionError("Admin authentication failed (wrong current password).")
        self.admin_pw_hash = hash_password(new_pw)

    # -- Users --
    def register_user(self, uid: str, password: str):
        if uid in self.users:
            raise ValueError("User already exists.")
        self.users[uid] = {
            'pw_hash': hash_password(password),
            'has_submitted': False,
        }

    def auth_user(self, uid: str, password: str) -> bool:
        user_record = self.users.get(uid)
        if not user_record:
            return False
        return user_record['pw_hash'] == hash_password(password)

    def auth_admin(self, password: str) -> bool:
        return self.admin_pw_hash == hash_password(password)

    # -- Complaint submission (auth BEFORE taking text) --
    def submit_complaint(self, uid: str, password: str, text: str):
        if uid not in self.users:
            raise PermissionError("User not registered. Please register first.")
        if not self.auth_user(uid, password):
            raise PermissionError("Authentication failed.")
        if self.users[uid]['has_submitted']:
            raise PermissionError("Already submitted a complaint.")

        iv, ct = aes_encrypt_pt(text, self.master_key_bytes)  # str -> bytes
        data_hash = sha256_hex(ct)  # integrity over the stored ciphertext

        self.bc.add_block(
            user_mask=mask_user_id(uid),
            uid_hash=hash_text(uid),
            key_hash=self.master_key_hash,
            iv_hex=iv.hex(),
            enc_hex=ct.hex(),
            data_hash=data_hash
        )
        self.users[uid]['has_submitted'] = True

    # -- Admin review (auth required) --
    def admin_list_decrypted(self, password: str):
        if not self.auth_admin(password):
            raise PermissionError("Admin authentication failed.")
        if not self.bc.is_valid():
            raise RuntimeError("Blockchain invalid.")

        out = []
        for b in self.bc.chain[1:]:  # skip genesis
            # Verify integrity of encrypted data first
            status = "ok" if sha256_hex(bytes.fromhex(b.enc_hex)) == b.data_hash else "tampered"
            text = "<undecryptable>"
            if status == "ok" and b.key_hash == self.master_key_hash:
                try:
                    iv = bytes.fromhex(b.iv_hex)
                    ct = bytes.fromhex(b.enc_hex)
                    text = aes_decrypt_ct(iv, ct, self.master_key_bytes)
                except Exception:
                    text = "<decrypt-error>"
            out.append({
                "user_mask": b.user_mask,
                "status": status,
                "text": text,
                "block": b.hash[:10] + "..."
            })
        return out
    
    def show_blockchain(self):
        for b in self.bc.chain[:]:
            print(f"Idx:{b.index} Prev:{b.prev_hash[:8]} Hash:{b.hash[:8]} User:{b.user_mask} H:{b.data_hash[:8]}")

    def list_users(self):
        return [{"uid": uid, "mask": mask_user_id(uid), "submitted": rec['has_submitted']} for uid, rec in self.users.items()]

    def export_chain_json(self) -> str:
        return json.dumps([asdict(b) for b in self.bc.chain], indent=2)

# ========================= CLI ============================
def main():
    app = ComplaintApp(master_key_str=MASTER_KEY, admin_password=ADMIN_DEFAULT_PASSWORD, difficulty=POW_DIFFICULTY)

    while True:
        print("\n=== Secure Complaint / Whistleblower System ===")
        print(f"Admin default password: {ADMIN_DEFAULT_PASSWORD}")
        print("1) Register user")
        print("2) Login & Submit complaint")
        print("3) Show blockchain (short)")
        print("4) Validate blockchain")
        print("5) Admin: Review Decrypted Complaints")
        print("6) Export blockchain (JSON to file + print)")
        print("7) Change Admin Password")
        print("8) List Users")
        print("0) Exit")
        choice = input("> ").strip()

        if choice == "1":
            uid = input("User ID: ").strip()
            pw = input("Password: ").strip()
            try:
                app.register_user(uid, pw)
                print("Registered.")
            except Exception as e:
                print("Error:", e)

        elif choice == "2":
            uid = input("User ID (must be registered): ").strip()
            if uid not in app.users:
                print("Error: User not registered. Please register first.")
                continue
            pw = input("Password: ").strip()
            if not app.auth_user(uid, pw):
                print("Error: Authentication failed.")
                continue
            text = input("Complaint text: ").strip()
            try:
                app.submit_complaint(uid, pw, text)
                print("Complaint recorded on blockchain.")
            except Exception as e:
                print("Error:", e)

        elif choice == "3":
            app.show_blockchain()

        elif choice == "4":
            print("Valid chain?:", app.bc.is_valid())

        elif choice == "5":
            apw = input("Admin password: ").strip()
            try:
                rows = app.admin_list_decrypted(apw)
                for r in rows:
                    print(f"{r['user_mask']}: {r['text']} ({r['status']}) #{r['block']}")
            except Exception as e:
                print("Error:", e)

        elif choice == "6":
            # Save to file AND print to CLI
            js = app.export_chain_json()
            try:
                with open(EXPORT_FILENAME, "w", encoding="utf-8") as f:
                    f.write(js)
                print(f"Blockchain saved to: {EXPORT_FILENAME}")
            except Exception as e:
                print("Could not save file:", e)
            print(js)

        elif choice == "7":
            old = input("Current ADMIN password: ").strip()
            new = input("New ADMIN password: ").strip()
            try:
                app.set_admin_password(old, new)
                print("Admin password updated.")
            except Exception as e:
                print("Error:", e)

        elif choice == "8":
            for r in app.list_users():
                print(f"{r['uid']} -> mask:{r['mask']} submitted:{r['submitted']}")

        elif choice == "0":
            print("Bye.")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
