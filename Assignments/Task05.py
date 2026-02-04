# Task05.py — Q5. Bit-Flipping Experiment (AES-CBC vs DES-CBC)

from Crypto.Cipher import AES, DES
from Crypto.Random import get_random_bytes

def pkcs7_pad(data: bytes, block_size: int) -> bytes:
    pad_len = block_size - (len(data) % block_size)
    return data + bytes([pad_len]) * pad_len

def pkcs7_unpad(padded: bytes, block_size: int) -> bytes:
    pad_len = padded[-1]
    if pad_len < 1 or pad_len > block_size or padded[-pad_len:] != bytes([pad_len]) * pad_len:
        raise ValueError("Invalid PKCS7 padding")
    return padded[:-pad_len]

def flip_one_bit(b: bytes, index: int = 0, bit: int = 0) -> bytes:
    # Flip a single bit (0..7) at byte index
    arr = bytearray(b)
    arr[index] ^= (1 << bit)
    return bytes(arr)

def diff_bytes(a: bytes, b: bytes) -> int:
    return sum(1 for x, y in zip(a, b) if x != y) + abs(len(a)-len(b))

def run_cipher(name, block_size, new, key_len, iv_len):
    msg = input(f"Enter a short message for {name}-CBC: ").encode('utf-8')
    key = get_random_bytes(key_len)
    iv = get_random_bytes(iv_len)
    cipher = new(key, mode=new.MODE_CBC, iv=iv)
    ct = cipher.encrypt(pkcs7_pad(msg, block_size))

    # Flip 1 bit in the first byte of ciphertext
    ct_flipped = flip_one_bit(ct, 0, 0)

    # Decrypt both
    dec_ok = new(key, mode=new.MODE_CBC, iv=iv).decrypt(ct)
    dec_bad = new(key, mode=new.MODE_CBC, iv=iv).decrypt(ct_flipped)

    pt_ok = pkcs7_unpad(dec_ok, block_size)
    # pkcs7_unpad may fail for dec_bad due to padding corruption;
    # in that case, show raw decrypted for the first block to observe avalanche.
    try:
        pt_bad = pkcs7_unpad(dec_bad, block_size)
        unpadded = True
    except Exception:
        pt_bad = dec_bad  # show raw to inspect
        unpadded = False

    print(f"\n=== {name}-CBC Results ===")
    print(f"Key: {key.hex()}")
    print(f"IV : {iv.hex()}")
    print("Ciphertext (hex):", ct.hex())
    print("Ciphertext (flipped one bit) (hex):", ct_flipped.hex())
    print("Decrypted (good) :", pt_ok)
    print("Decrypted (flipped):", pt_bad)
    if unpadded:
        print("Changed bytes in plaintext after one-bit flip:", diff_bytes(pt_ok, pt_bad))
    else:
        # Compare first block to show local corruption + next-block effect
        print("First block (good)     :", dec_ok[:block_size].hex())
        print("First block (flipped)  :", dec_bad[:block_size].hex())
        print("Second block (good)    :", dec_ok[block_size:2*block_size].hex())
        print("Second block (flipped) :", dec_bad[block_size:2*block_size].hex())

def main():
    # AES: 16-byte block, key 16, IV 16
    run_cipher("AES", 16, AES.new, 16, 16)
    # DES: 8-byte block, key 8, IV 8
    run_cipher("DES", 8, DES.new, 8, 8)

    print("\nExplanation (4–5 lines):")
    print("- In CBC, flipping one bit in ciphertext corrupts the entire decrypted block and flips the corresponding bit in the next block.")
    print("- AES has a 16-byte block; DES has an 8-byte block. Larger blocks mean a larger region is fully corrupted under the same error event.")
    print("- Apart from block size, AES uses a stronger round function; but error propagation in CBC is mode-driven, not algorithm-driven.")
    print("- Padding often becomes invalid after bit flips, causing decryption to fail at unpadding; inspecting raw blocks shows the propagation pattern.")

if __name__ == "__main__":
    main()