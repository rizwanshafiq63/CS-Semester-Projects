import hashlib
import time

class ProofOfWork:
    def __init__(self, block_data, difficulty=4):
        self.block_data = block_data
        self.difficulty = difficulty  # Number of leading zeros required
        self.target = "0" * difficulty

    def mine(self):
        """Find a nonce that produces a hash with required difficulty"""
        nonce = 0
        start_time = time.time()

        while True:
            # Combine block data with nonce
            hash_input = f"{self.block_data}{nonce}"
            hash_result = hashlib.sha256(hash_input.encode()).hexdigest()

            # Check if hash meets difficulty requirement
            if hash_result.startswith(self.target):
                end_time = time.time()
                return nonce, hash_result, end_time - start_time

            nonce += 1

            # Show progress every 100,000 attempts
            if nonce % 100000 == 0:
                print(f"Attempt {nonce}... Current hash: {hash_result[:20]}...")

# Example: Mining a block
block_data = "Alice → Bob: 10 BTC | Timestamp: 2025-10-12"
pow = ProofOfWork(block_data, difficulty=10)

print("Mining started...")
nonce, final_hash, time_taken = pow.mine()

print(f"\n✓ Block mined!")
print(f"Nonce found: {nonce}")
print(f"Final hash: {final_hash}")
print(f"Time taken: {time_taken:.2f} seconds")
print(f"Hash starts with {pow.difficulty} zeros: {final_hash.startswith(pow.target)}")