# Task04 — Q4 (Revised): Automatic same-folder file handling.
# When you run this script, it will:
#  1) Read 'input.txt' from the same folder (create a sample if missing).
#  2) Encrypt first half with AES-CBC and second half with DES-ECB.
#  3) Write 'encrypted.bin' and 'meta.json' in the same folder.
#  4) Decrypt back to 'recovered.txt' to verify.

from pathlib import Path
import json
from Crypto.Cipher import AES, DES
from Crypto.Random import get_random_bytes

HERE = Path(__file__).resolve().parent
INPUT_PATH = HERE / "input.txt"
ENC_PATH = HERE / "encrypted.bin"
HELPER_PATH = HERE / "meta.json"
RECOVERED_PATH = HERE / "recovered.txt"

def pkcs7_pad(data: bytes, block_size: int) -> bytes:
    pad_len = block_size - (len(data) % block_size)
    return data + bytes([pad_len]) * pad_len

def pkcs7_unpad(padded: bytes, block_size: int) -> bytes:
    pad_len = padded[-1]
    if pad_len < 1 or pad_len > block_size or padded[-pad_len:] != bytes([pad_len]) * pad_len:
        raise ValueError("Invalid PKCS7 padding")
    return padded[:-pad_len]

def ensure_input():
    if not INPUT_PATH.exists():
        INPUT_PATH.write_text(
            "This is a demo plaintext for Task 04.\n"
            "The first half will be encrypted with AES-CBC.\n"
            "The second half will be encrypted with DES-ECB.\n",
            encoding="utf-8"
        )
        print(f"[+] Created sample {INPUT_PATH.name}")
    else:
        print(f"[*] Found {INPUT_PATH.name}")

def encrypt():
    data = INPUT_PATH.read_bytes()
    n = len(data)
    mid = n // 2
    first = data[:mid]
    second = data[mid:]

    # AES-CBC for first half
    aes_key = get_random_bytes(16)
    aes_iv = get_random_bytes(16)
    aes = AES.new(aes_key, AES.MODE_CBC, aes_iv)
    first_ct = aes.encrypt(pkcs7_pad(first, 16))

    # DES-ECB for second half
    des_key = get_random_bytes(8)
    des = DES.new(des_key, DES.MODE_ECB)
    second_ct = des.encrypt(pkcs7_pad(second, 8))

    combined = first_ct + second_ct
    ENC_PATH.write_bytes(combined)

    meta = {
        "orig_len": n,
        "split_index": mid,
        "aes_key_hex": aes_key.hex(),
        "aes_iv_hex": aes_iv.hex(),
        "des_key_hex": des_key.hex(),
        "first_ct_len": len(first_ct),
        "second_ct_len": len(second_ct)
    }
    HELPER_PATH.write_text(json.dumps(meta, indent=2))
    print(f"[+] Encrypted -> {ENC_PATH.name}, {HELPER_PATH.name}")

def decrypt():
    combined = ENC_PATH.read_bytes()
    meta = json.loads(HELPER_PATH.read_text())

    first_ct_len = meta["first_ct_len"]
    first_ct = combined[:first_ct_len]
    second_ct = combined[first_ct_len:]

    aes_key = bytes.fromhex(meta["aes_key_hex"])
    aes_iv = bytes.fromhex(meta["aes_iv_hex"])
    des_key = bytes.fromhex(meta["des_key_hex"])

    aes = AES.new(aes_key, AES.MODE_CBC, aes_iv)
    first_pt = pkcs7_unpad(aes.decrypt(first_ct), 16)

    des = DES.new(des_key, DES.MODE_ECB)
    second_pt = pkcs7_unpad(des.decrypt(second_ct), 8)

    recovered = first_pt + second_pt
    RECOVERED_PATH.write_bytes(recovered)
    print(f"[+] Decrypted -> {RECOVERED_PATH.name}")
    if len(recovered) != meta["orig_len"]:
        print("[!] Warning: recovered length differs from original length recorded in metadata.")
    else:
        print("[*] Length check OK.")

def main():
    ensure_input()
    encrypt()
    decrypt()
    print("\nDone. Place your own plaintext in 'input.txt' and run again if you like.")

if __name__ == "__main__":
    main()
