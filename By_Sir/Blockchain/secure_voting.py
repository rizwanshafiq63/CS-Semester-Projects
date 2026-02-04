import hashlib
import json
import time
from dataclasses import dataclass, asdict

# Try to import AES (PyCryptodome). If unavailable, we will use Vigenere fallback.
try:
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import pad, unpad
    HAS_AES = True
except Exception:
    HAS_AES = False

# utilities
def sha256_hex(data_bytes: bytes) -> str:
    # return sha256 hex digest for given bytes.
    return hashlib.sha256(data_bytes).hexdigest()

def mask_voter_id(voter_id: str) -> str:
    # mask voter id when storing on-chain.
    if len(voter_id) <= 4:
        return "****"
    return voter_id[:2] + "*"*(len(voter_id)-4) + voter_id[-2:]


# encryption helpers
# AES helpers (CBC with PKCS7 via pad/unpad)
def aes_encrypt(plaintext: str, key_bytes: bytes) -> bytes:
    # key_bytes should be 16 bytes for AES-128
    key = key_bytes[:16]
    # derive IV as first 16 bytes of SHA256(key + timestamp) for demo (in real: os.urandom(16))
    iv = hashlib.sha256(key_bytes + str(time.time()).encode()).digest()[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ct = cipher.encrypt(pad(plaintext.encode(), AES.block_size))
    return iv + ct  # prefix IV so it can be extracted for decryption

def aes_decrypt(iv_and_ct: bytes, key_bytes: bytes) -> str:
    # decrypt IV + ciphertext using AES; returns plaintext string.
    key = key_bytes[:16]
    iv = iv_and_ct[:16]
    ct = iv_and_ct[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), AES.block_size)
    return pt.decode()

def vigenere_encrypt(plaintext: str, key: str) -> str:
    res = []
    key = key.upper()
    klen = len(key)
    j = 0
    for ch in plaintext:
        if ch.isalpha():
            base = 'A' if ch.isupper() else 'a'
            p = ord(ch) - ord(base)
            k = ord(key[j % klen]) - ord('A')
            c = (p + k) % 26
            res.append(chr(c + ord(base)))
            j += 1
        else:
            res.append(ch)
    return ''.join(res)

def vigenere_decrypt(ciphertext: str, key: str) -> str:
    res = []
    key = key.upper()
    klen = len(key)
    j = 0
    for ch in ciphertext:
        if ch.isalpha():
            base = 'A' if ch.isupper() else 'a'
            c = ord(ch) - ord(base)
            k = ord(key[j % klen]) - ord('A')
            p = (c - k) % 26
            res.append(chr(p + ord(base)))
            j += 1
        else:
            res.append(ch)
    return ''.join(res)

# key derivation helper (from password to AES key bytes)
def derive_key_from_password(password: str) -> bytes:
    #derive a 32-byte-ish key bytes from password using SHA256.
    return hashlib.sha256(password.encode()).digest()


#blockchain classes
@dataclass
class Block:
    index: int
    timestamp: float
    voter_mask: str
    encrypted_vote_hex: str
    vote_hash: str
    previous_hash: str
    nonce: int = 0
    hash: str = ""

    def compute_hash(self) -> str:
        block_string = f"{self.index}{self.timestamp}{self.voter_mask}{self.encrypted_vote_hex}{self.vote_hash}{self.previous_hash}{self.nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine(self, difficulty: int = 2):
        # Proof-of-Work: find nonce so that hash starts with '0'*difficulty.
        prefix = '0' * difficulty
        self.nonce = 0
        while True:
            self.hash = self.compute_hash()
            if self.hash.startswith(prefix):
                return
            self.nonce += 1

class Blockchain:
    def __init__(self, difficulty: int = 2):
        self.chain = []
        self.difficulty = difficulty
        # create genesis
        genesis = Block(0, time.time(), "GENESIS", "", "", "0", 0, "")
        genesis.hash = genesis.compute_hash()
        self.chain.append(genesis)

    def add_block(self, voter_mask: str, encrypted_vote_hex: str, vote_hash: str):
        last = self.chain[-1]
        new_block = Block(index=len(self.chain),
                          timestamp=time.time(),
                          voter_mask=voter_mask,
                          encrypted_vote_hex=encrypted_vote_hex,
                          vote_hash=vote_hash,
                          previous_hash=last.hash)
        new_block.mine(self.difficulty)
        self.chain.append(new_block)
        return new_block

    def is_valid(self) -> bool:
        for i in range(1, len(self.chain)):
            cur = self.chain[i]
            prev = self.chain[i-1]
            if cur.previous_hash != prev.hash:
                print("Previous hash mismatch at index", i)
                return False
            if cur.compute_hash() != cur.hash:
                print("Hash mismatch at index", i)
                return False
        return True

    def to_json(self):
        return json.dumps([asdict(b) for b in self.chain], indent=2)

# Voting System
class VotingSystem:
    def __init__(self, use_aes=True, difficulty=2):
        self.voters_db = {}  # voter_id -> {'password':..., 'has_voted':False}
        self.blockchain = Blockchain(difficulty=difficulty)
        self.use_aes = use_aes and HAS_AES
        if use_aes and not HAS_AES:
            print("pycryptodome not available, AES disabled, using Vigenere.")

    def register_voter(self, voter_id: str, password: str):
        if voter_id in self.voters_db:
            raise ValueError("Voter already registered")
        # store password hash instead of plain password
        pwd_hash = sha256_hex(password.encode())
        self.voters_db[voter_id] = {'password_hash': pwd_hash, 'has_voted': False}
        return True

    def authenticate(self, voter_id: str, password: str) -> bool:
        rec = self.voters_db.get(voter_id)
        if not rec:
            return False
        return rec['password_hash'] == sha256_hex(password.encode())

    def cast_vote(self, voter_id: str, password: str, vote_text: str, vigenere_key: str = "DEFAULT"):
        # 1. authenticate
        if not self.authenticate(voter_id, password):
            raise PermissionError("Authentication failed")
        if self.voters_db[voter_id]['has_voted']:
            raise PermissionError("Voter has already cast a vote")

        # 2. encrypt vote
        if self.use_aes:
            key_bytes = derive_key_from_password(password)
            ciphertext_bytes = aes_encrypt(vote_text, key_bytes)  # iv+ct bytes
            encrypted_hex = ciphertext_bytes.hex()
        else:
            # fallback to Vigenere; store ascii text
            encrypted_text = vigenere_encrypt(vote_text, vigenere_key)
            encrypted_hex = encrypted_text.encode().hex()

        # 3. compute hash of encrypted vote
        vote_hash = sha256_hex(bytes.fromhex(encrypted_hex))

        # 4. store on blockchain (voter masked)
        voter_mask = mask_voter_id(voter_id)
        block = self.blockchain.add_block(voter_mask, encrypted_hex, vote_hash)

        # 5. mark voter as voted
        self.voters_db[voter_id]['has_voted'] = True

        return block

    def tally_votes(self, password_lookup: dict = None, vigenere_key: str = "DEFAULT"):
        """
        Tally votes. For AES, password_lookup must map voter_id -> password to derive AES keys.
        For Vigenere fallback, provide the vigenere_key.
        Returns dict: {candidate_or_vote_text: count}
        """
        counts = {}
        # verify blockchain integrity first
        if not self.blockchain.is_valid():
            raise RuntimeError("Blockchain invalid - abort tally")

        # skip genesis
        for block in self.blockchain.chain[1:]:
            enc_hex = block.encrypted_vote_hex
            # recompute and verify hash
            recomputed_hash = sha256_hex(bytes.fromhex(enc_hex))
            if recomputed_hash != block.vote_hash:
                print(f"Tamper detected in block {block.index} (hash mismatch). Skipping.")
                continue  # skip tampered

            # decrypt
            if self.use_aes:
                # Need to know which voter/password -> in simple system we require password_lookup
                if not password_lookup:
                    raise ValueError("Password lookup required to decrypt AES votes for tally.")
                # We only have masked voter id on the chain; so we must map masked->voter id externally.
                # Here assume password_lookup provides 'voter_id' -> password for all voters in this run.
                # For demo, we'll attempt to decrypt with every password until one yields sensible plaintext.
                decrypted = None
                for vid, pwd in password_lookup.items():
                    try:
                        keyb = derive_key_from_password(pwd)
                        dec = aes_decrypt(bytes.fromhex(enc_hex), keyb)
                        # If decrypt succeeds without exception, accept it
                        decrypted = dec
                        break
                    except Exception:
                        continue
                if decrypted is None:
                    decrypted = "<undecryptable>"
            else:
                decrypted = vigenere_decrypt(bytes.fromhex(enc_hex).decode(), vigenere_key)

            counts[decrypted] = counts.get(decrypted, 0) + 1

        return counts


def demo():
    vs = VotingSystem(use_aes=True, difficulty=2)

    # Register voters
    vs.register_voter("alice01", "alicepass")
    vs.register_voter("bob02", "bobpass")
    vs.register_voter("carol03", "carolpass")

    # Cast votes
    print("Alice votes for 'Candidate A'")
    block_a = vs.cast_vote("alice01", "alicepass", "Candidate A")

    print("Bob votes for 'Candidate B'")
    block_b = vs.cast_vote("bob02", "bobpass", "Candidate B")

    print("Carol votes for 'Candidate A'")
    block_c = vs.cast_vote("carol03", "carolpass", "Candidate A")

    print("\nBlockchain snapshot (short):")
    for b in vs.blockchain.chain:
        print(f"Index:{b.index} PrevHash:{b.previous_hash[:8]} Hash:{b.hash[:8]} Voter:{b.voter_mask} VoteHash:{b.vote_hash[:8]}")

    # Tally (provide password lookup to decrypt AES votes)
    password_lookup = {"alice01": "alicepass", "bob02": "bobpass", "carol03": "carolpass"}
    results = vs.tally_votes(password_lookup=password_lookup)
    print("\nTally results:")
    print(results)

    # Verify blockchain validity
    print("\nBlockchain valid?", vs.blockchain.is_valid())

if __name__ == "__main__":
    demo()