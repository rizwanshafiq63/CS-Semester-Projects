import hashlib
import time

def mine_block(data, difficulty):
    nonce = 0
    prefix = "0" * difficulty
    start = time.time()

    while True:
        hash_result = hashlib.sha256((data + str(nonce)).encode()).hexdigest()
        if hash_result.startswith(prefix):
            end = time.time()
            print(f"Mined! Difficulty={difficulty}, Nonce={nonce}, Time={round(end-start, 2)}s")
            print("Hash:", hash_result)
            break
        nonce += 1

mine_block("Ali pays Majid 2 BTC", difficulty=3)
print()
mine_block("Ali pays Majid 2 BTC", difficulty=7)