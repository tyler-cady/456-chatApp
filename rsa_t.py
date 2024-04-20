import random
import math

def is_prime(n, k=40):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def miller_rabin(n, k=40):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def genPrime(bit_length):
    while True:
        candidate = random.getrandbits(bit_length)
        candidate |= (1 << (bit_length - 1)) | 1  # Ensure that the number is odd and has the correct bit length
        if miller_rabin(candidate):
            return candidate

def genKeys(bit_length):
    p = genPrime(bit_length // 2)
    while True:
        q = genPrime(bit_length // 2)
        if p != q:  # Ensure p and q are distinct
            break
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537
    d = modinv(e, phi)
    public_key = (n, e)
    private_key = (n, d)
    return public_key, private_key

def encrypt(message, pub_key):
    (n, e) = pub_key
    if isinstance(message, bytes):
        message = int.from_bytes(message, byteorder='big')
    encrypted = pow(message, e, n)
    return encrypted.to_bytes((encrypted.bit_length() + 7) // 8, byteorder='big')

def decrypt(private_key, encrypted_message):
    n, d = private_key
    if isinstance(encrypted_message, bytes):
        encrypted_message = int.from_bytes(encrypted_message, byteorder='big')
    decrypted = pow(encrypted_message, d, n)
    return decrypted.to_bytes((decrypted.bit_length() + 7) // 8, byteorder='big')

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('Modular inverse does not exist')
    else:
        return x % m
def main():
    # Generate public and private keys
    public_key, private_key = genKeys(4096)

    # Encrypt a message
    message = b"Hello, world!"
    encrypted_message = encrypt(message, public_key)
    print("Encrypted message:", encrypted_message)

    # Decrypt the encrypted message
    decrypted_message = decrypt(private_key, encrypted_message)
    print("Decrypted message:", decrypted_message.decode())

if __name__ == "__main__":
    main()
