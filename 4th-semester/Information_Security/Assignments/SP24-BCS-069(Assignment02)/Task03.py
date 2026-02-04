# Task03 — Q3. AES vs DES Block Size Analysis (ECB)

from Crypto.Cipher import AES, DES
from Crypto.Random import get_random_bytes

def pkcs7_pad(data: bytes, block_size: int) -> bytes:
    pad_len = block_size - (len(data) % block_size)
    return data + bytes([pad_len]) * pad_len

def main():
    text = input("Enter plaintext: ").encode('utf-8')

    aes_key = get_random_bytes(16)  # 128-bit
    des_key = get_random_bytes(8)   # 64-bit key 

    aes_ecb = AES.new(aes_key, AES.MODE_ECB)
    des_ecb = DES.new(des_key, DES.MODE_ECB)

    ct_aes = aes_ecb.encrypt(pkcs7_pad(text, 16))
    ct_des = des_ecb.encrypt(pkcs7_pad(text, 8))

    print("AES-ECB ciphertext (hex):", ct_aes.hex())
    print("DES-ECB ciphertext (hex):", ct_des.hex())

    print("\nBlock sizes: AES = 128 bits (16 bytes), DES = 64 bits (8 bytes).")
    print("Why AES is more secure than DES (beyond key size):")
    print("1) Stronger round function and S-box design; resistant to known cryptanalytic attacks like differential/linear.")
    print("2) Larger block size reduces risks like block collisions and pattern leakage in ECB.")
    print("3) Simpler, well-analyzed structure (SubBytes/ShiftRows/MixColumns/AddRoundKey) with no known practical weaknesses.")

if __name__ == "__main__":
    main()
