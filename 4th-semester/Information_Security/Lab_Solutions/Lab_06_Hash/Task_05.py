# Task 05: Hash Stretching

import hashlib

password = b"CorrectHorseBatteryStaple!"
salt = bytes.fromhex("0123456789abcdeffedcba9876543210")
dklen = 32           # 256-bit
iterations = 100_000

key = hashlib.pbkdf2_hmac('sha256', password, salt, iterations, dklen=dklen)
print(key.hex())
