# Primality Testing with the Rabin–Miller Algorithm
import random


def rabinMiller(num):
    """
    Returns True if num is a prime number using Rabin–Miller test.

    Args:
        num: Number to test for primality
    Returns:
        True if probably prime, False if composite
    """
    s = num - 1
    t = 0

    # Keep halving s while it is even
    # Count how many times we halve s in t
    while s % 2 == 0:
        s = s // 2
        t += 1

    # Try to falsify num's primality 5 times
    for _ in range(5):
        a = random.randrange(2, num - 1)
        v = pow(a, s, num)

        if v != 1:  # This test does not apply if v is 1
            i = 0
            while v != (num - 1):
                if i == t - 1:
                    return False  # num is composite
                else:
                    i = i + 1
                    v = (v ** 2) % num

    return True  # num is probably prime


def isPrime(num):
    """
    Checks whether a number is prime using trial division and the Rabin–Miller test.

    Args:
        num: Number to test
    Returns:
        True if prime, False otherwise
    """
    if num < 2:
        return False  # 0, 1, and negative numbers are not prime

    # List of the first 168 prime numbers
    lowPrimes = [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47,
        53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107,
        109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167,
        173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229,
        233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283,
        293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359,
        367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431,
        433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491,
        499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571,
        577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641,
        643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709,
        719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787,
        797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859,
        863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941,
        947, 953, 967, 971, 977, 983, 991, 997
    ]

    # Check if num is in the list of low primes
    if num in lowPrimes:
        return True

    # See if any of the low prime numbers can divide num
    for prime in lowPrimes:
        if num % prime == 0:
            return False

    # If all else fails, call rabinMiller() to determine if num is prime
    return rabinMiller(num)


def generateLargePrime(keysize):
    """
    Return a random prime number of keysize bits in size.

    Args:
        keysize: Number of bits in the prime
    Returns:
        A prime number with keysize bits
    """
    while True:
        # Generate random number in range [2^(keysize-1), 2^keysize)
        num = random.randrange(2 ** (keysize - 1), 2 ** keysize)
        if isPrime(num):
            return num
