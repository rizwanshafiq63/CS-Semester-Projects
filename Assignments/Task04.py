# Task04.py — Q4. File Fragment Encryption with AES (CBC) and DES (ECB)
# Modes:
#   Encrypt: python Task04.py e <input.txt> <out.bin> <meta.json>
#   Decrypt: python Task04.py d <in.bin> <meta.json> <recovered.txt>

import sys
import json
from Crypto.Cipher import AES, DES
from Crypto.Random import get_random_bytes
from pathlib import Path

def pkcs7_pad(data: bytes, block_size: int) -> bytes:
    pad_len = block_size - (len(data) % block_size)
    return data + bytes([pad_len]) * pad_len

def pkcs7_unpad(padded: bytes, block_size: int) -> bytes:
    pad_len = padded[-1]
    if pad_len < 1 or pad_len > block_size or padded[-pad_len:] != bytes([pad_len]) * pad_len:
        raise ValueError("Invalid PKCS7 padding")
    return padded[:-pad_len]

def encrypt(input_path: str, out_path: str, meta_path: str):
    data = Path(input_path).read_bytes()
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
    Path(out_path).write_bytes(combined)

    meta = {
        "orig_len": n,
        "split_index": mid,
        "aes_key_hex": aes_key.hex(),
        "aes_iv_hex": aes_iv.hex(),
        "des_key_hex": des_key.hex(),
        "first_ct_len": len(first_ct),  # boundary to split combined file
        "second_ct_len": len(second_ct)
    }
    Path(meta_path).write_text(json.dumps(meta, indent=2))
    print("Encrypted. Wrote:", out_path, "and", meta_path)

def decrypt(in_path: str, meta_path: str, out_path: str):
    combined = Path(in_path).read_bytes()
    meta = json.loads(Path(meta_path).read_text())

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
    Path(out_path).write_bytes(recovered)
    print("Decrypted. Wrote:", out_path)
    if len(recovered) != meta["orig_len"]:
        print("Warning: recovered length differs from original length recorded in metadata.")

def main():
    if len(sys.argv) < 5:
        print("Usage:")
        print("  Encrypt: python Task04.py e <input.txt> <out.bin> <meta.json>")
        print("  Decrypt: python Task04.py d <in.bin> <meta.json> <recovered.txt>")
        sys.exit(1)
    mode = sys.argv[1].lower()
    if mode == 'e':
        _, _, inp, outp, metap = sys.argv
        encrypt(inp, outp, metap)
    elif mode == 'd':
        _, _, inp, metap, outp = sys.argv
        decrypt(inp, metap, outp)
    else:
        print("Unknown mode; use 'e' or 'd'")
        sys.exit(1)

if __name__ == "__main__":
    main()