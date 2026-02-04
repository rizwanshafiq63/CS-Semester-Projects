import hashlib

data = "Alice sends 2 BTC to BoB"
nonce = 0

while True:
    hash_result = hashlib.sha256((data + str(nonce)).encode()).hexdigest()
    if hash_result.startswith("00"):
        print("✅ Valid Hash Found:", hash_result)
        print("Nonce used:", nonce)
        break
    print(nonce)
    print(hash_result)
    nonce += 1