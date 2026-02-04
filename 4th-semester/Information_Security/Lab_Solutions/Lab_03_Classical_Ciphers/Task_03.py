# Lab 3 – Classical Ciphers Toolkit (Caesar + Vigenère)
# Features:
# - Caesar: encrypt/decrypt + brute-force (frequency ranking)
# - Vigenère: encrypt/decrypt, Friedman IC key-length guess, blind break (chi-squared),
#   known-plaintext (crib) key recovery.
#
# This aligns with Lab 3 outcomes: classical ciphers + cryptanalysis (frequency, known-plaintext).

import re
import math
from collections import Counter, defaultdict
from typing import List, Tuple

A = ord('A')

# -----------------------------
# Helpers
# -----------------------------
def normalize(text: str, letters_only: bool = True) -> str:
    """Uppercase; optionally keep only A–Z (improves classical-cipher analysis)."""
    t = text.upper()
    return re.sub(r'[^A-Z]', '', t) if letters_only else t

EN_FREQ_RAW = {
    'A': 8.167, 'B': 1.492, 'C': 2.782, 'D': 4.253, 'E': 12.702, 'F': 2.228, 'G': 2.015,
    'H': 6.094, 'I': 6.966, 'J': 0.153, 'K': 0.772, 'L': 4.025, 'M': 2.406, 'N': 6.749,
    'O': 7.507, 'P': 1.929, 'Q': 0.095, 'R': 5.987, 'S': 6.327, 'T': 9.056, 'U': 2.758,
    'V': 0.978, 'W': 2.360, 'X': 0.150, 'Y': 1.974, 'Z': 0.074
}
_TOTAL = sum(EN_FREQ_RAW.values())
EN_FREQ = {k: v / _TOTAL for k, v in EN_FREQ_RAW.items()}  # normalize to 1.0

def shift_char(ch: str, k: int) -> str:
    return chr((ord(ch) - A + k) % 26 + A)

def chi_squared_stat(text: str) -> float:
    """Chi-squared distance of text letter distribution vs English."""
    N = len(text)
    if N == 0:
        return float('inf')
    counts = Counter(text)
    chi = 0.0
    for letter in EN_FREQ:
        expected = EN_FREQ[letter] * N
        observed = counts.get(letter, 0)
        chi += (observed - expected) ** 2 / expected if expected > 0 else 0.0
    return chi

def index_of_coincidence(text: str) -> float:
    """IC = sum(n_i(n_i-1)) / (N(N-1))"""
    N = len(text)
    if N < 2:
        return 0.0
    counts = Counter(text)
    return sum(n*(n-1) for n in counts.values()) / (N*(N-1))

# -----------------------------
# Caesar
# -----------------------------
def caesar_encrypt(pt: str, k: int) -> str:
    pt = normalize(pt)
    return ''.join(shift_char(c, k) for c in pt)

def caesar_decrypt(ct: str, k: int) -> str:
    ct = normalize(ct)
    return ''.join(shift_char(c, -k) for c in ct)

def caesar_bruteforce(ct: str, top: int = 5) -> List[Tuple[int, str, float]]:
    """Try all shifts; return best by chi-squared: (shift, plaintext, chi2)."""
    ct = normalize(ct)
    results = []
    for k in range(26):
        pt_guess = caesar_decrypt(ct, k)
        results.append((k, pt_guess, chi_squared_stat(pt_guess)))
    results.sort(key=lambda x: x[2])
    return results[:top]

# -----------------------------
# Vigenère
# -----------------------------
def vigenere_encrypt(pt: str, key: str) -> str:
    pt = normalize(pt)
    key = normalize(key)
    out = []
    for i, ch in enumerate(pt):
        k = ord(key[i % len(key)]) - A
        out.append(shift_char(ch, k))
    return ''.join(out)

def vigenere_decrypt(ct: str, key: str) -> str:
    ct = normalize(ct)
    key = normalize(key)
    out = []
    for i, ch in enumerate(ct):
        k = ord(key[i % len(key)]) - A
        out.append(shift_char(ch, -k))
    return ''.join(out)

def _columns(text: str, keylen: int) -> List[str]:
    return [''.join(text[i] for i in range(j, len(text), keylen)) for j in range(keylen)]

def friedman_keylen_guesses(ct: str, max_len: int = 20) -> List[Tuple[int, float]]:
    """Average IC across columns for each key length. Sort by closeness to ~0.066 (English mono)."""
    target = 0.066
    ct = normalize(ct)
    scores = []
    for k in range(1, max_len+1):
        cols = _columns(ct, k)
        avg_ic = sum(index_of_coincidence(col) for col in cols) / k
        scores.append((k, avg_ic))
    scores.sort(key=lambda x: abs(x[1] - target))
    return scores

def kasiski_candidates(ct: str, min_l: int = 3, max_l: int = 5, top: int = 10) -> List[Tuple[int, int]]:
    """Optional: Kasiski (GCD of repeated n-gram distances) -> candidate key lengths."""
    ct = normalize(ct)
    positions = defaultdict(list)
    for L in range(min_l, max_l+1):
        for i in range(len(ct)-L+1):
            sub = ct[i:i+L]
            positions[sub].append(i)
    dists = []
    for idxs in positions.values():
        if len(idxs) > 1:
            for i in range(len(idxs)-1):
                dists.append(idxs[i+1]-idxs[i])
    gcd_counts = Counter()
    for i in range(len(dists)):
        for j in range(i+1, len(dists)):
            g = math.gcd(dists[i], dists[j])
            if g > 1:
                gcd_counts[g] += 1
    return gcd_counts.most_common(top)

def recover_vigenere_key_by_length(ct: str, keylen: int) -> Tuple[str, List[int]]:
    """Solve each column as a Caesar using chi-squared. Returns ('A=0' letters key, shifts list)."""
    ct = normalize(ct)
    shifts = []
    for col in _columns(ct, keylen):
        # try all inverse shifts and score decoded column
        best_shift = min(range(26), key=lambda s: chi_squared_stat(''.join(shift_char(c, -s) for c in col)))
        shifts.append(best_shift)
    key_letters = ''.join(chr(A + s) for s in shifts)  # 'A' means shift 0, 'B' means 1, etc.
    return key_letters, shifts

def vigenere_break(ct: str, max_keylen: int = 20, top_k: int = 3) -> List[Tuple[int, str, float, str]]:
    """Blind crack: try key lengths (Friedman order), solve columns, rank plaintext by chi-squared.
       Returns: (keylen, key_letters(A=0), chi2, plaintext) for top_k guesses.
    """
    ct = normalize(ct)
    candidates = []
    for klen, _ic in friedman_keylen_guesses(ct, max_keylen):
        key_letters, _ = recover_vigenere_key_by_length(ct, klen)
        pt_guess = vigenere_decrypt(ct, key_letters)
        score = chi_squared_stat(pt_guess)
        candidates.append((klen, key_letters, score, pt_guess))
    candidates.sort(key=lambda x: x[2])
    return candidates[:top_k]

def known_plaintext_recover_key(pt: str, ct: str, keylen: int) -> str:
    """Recover Vigenère key (A=0 letters) given a known plaintext block aligned at start (length ≥ keylen)."""
    pt = normalize(pt)
    ct = normalize(ct)
    if len(pt) < keylen or len(ct) < keylen:
        raise ValueError("Need ≥ keylen characters of known PT/CT from the start.")
    shifts = [(ord(c) - ord(p)) % 26 for p, c in zip(pt[:keylen], ct[:keylen])]
    return ''.join(chr(A + s) for s in shifts)

# -----------------------------
# Demo (feel free to change text/key)
# -----------------------------
if __name__ == "__main__":
    demo = "We hold these truths to be self-evident, that all men are created equal."
    key = "DECLARATION"

    print("=== VIGENÈRE DEMO ===")
    pt = normalize(demo)
    ct = vigenere_encrypt(pt, key)
    print("Plaintext (norm):", pt)
    print("Key:              ", key)
    print("Ciphertext:       ", ct)
    print("Decrypted:        ", vigenere_decrypt(ct, key))

    print("\n--- Blind Vigenère break (short texts can be unstable) ---")
    for i, (klen, kletters, score, guess) in enumerate(vigenere_break(ct, max_keylen=20, top_k=3), 1):
        print(f"[{i}] keylen={klen:2d} key(A=0)={kletters} chi2={score:.2f}  PT[:60]={guess[:60]}")

    print("\n--- Known-plaintext recovery (crib) ---")
    recovered_key = known_plaintext_recover_key(pt, ct, len(key))
    print("Recovered key (A=0 letters):", recovered_key)
    print("Recovered plaintext matches:", vigenere_decrypt(ct, recovered_key) == pt)

    print("\n=== CAESAR DEMO ===")
    c_ct = caesar_encrypt(pt, 3)
    print("Caesar(shift=3) CT:", c_ct)
    print("\nTop Caesar brute-force guesses:")
    for k, ptx, chi in caesar_bruteforce(c_ct, top=5):
        print(f"shift={k:2d} chi2={chi:7.2f} PT[:60]={ptx[:60]}")
