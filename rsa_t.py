import math
import random
import gmpy2


def genKeys(bit_length):
    p = genPrime(bit_length)
    q = genPrime(bit_length)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = getCoprime(phi)
    d = gmpy2.invert(e, phi)
    public_key = (n, e)
    private_key = (n, d)
    return public_key, private_key

def genPrime(bit_length):
    while True:
        candidate = random.getrandbits(bit_length)
        if gmpy2.is_prime(candidate):
            return candidate

def getCoprime(n):
    for e in range(2, n):
        if gmpy2.gcd(e, n) == 1:
            return e

def encrypt(public_key, message):
    n, e = public_key
    encrypted = pow(message, e, n)
    return encrypted

def decrypt(private_key, encrypted_message):
    n, d = private_key
    decrypted = pow(encrypted_message, d, n)
    return decrypted

