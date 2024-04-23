import os
from Crypto.Cipher import AES, DES
from Crypto.Util.Padding import pad, unpad
import hashlib
class AES_DES:
    def __init__(self, isAES=True):
        self.isAES = isAES

    def encrypt_m(self, message, key):
        if self.isAES:
            cipher = AES.new(key, AES.MODE_ECB)
            padded_message = pad(message.encode(), AES.block_size)
            return cipher.encrypt(padded_message)
        else:
            cipher = DES.new(key, DES.MODE_ECB)
            padded_message = pad(message.encode(), DES.block_size)
            return cipher.encrypt(padded_message)

    def decrypt_m(self, message, key):
        if self.isAES:
            cipher = AES.new(key, AES.MODE_ECB)
            decrypted_message = cipher.decrypt(message)
            return self.unpad_message(decrypted_message)
        else:
            cipher = DES.new(key, DES.MODE_ECB)
            decrypted_message = cipher.decrypt(message)
            return self.unpad_message(decrypted_message)



    def pad_message(self, message):
        block_size = AES.block_size if self.isAES else DES.block_size
        padding_size = block_size - len(message) % block_size
        padding = bytes([padding_size] * padding_size)
        return message.encode() + padding

    def unpad_message(self, message):
        padding_size = message[-1]
        return message[:-padding_size]
    
    def generate_key(passphrase, salt, key_length=32, iterations=100000):
        derived_key = hashlib.pbkdf2_hmac('sha256', passphrase.encode(), salt, iterations, dklen=key_length)
        return derived_key

def test_aes_des():
    message = "Test message"
    empty_message = ""
    long_message = "This is a long message. " * 1000  # Create a long message for testing

    # Generate keys using passphrase and salt
    passphrase = "HowdyPartner!"
    salt = os.urandom(16)  # Generate a random salt
    key_aes_128 = AES_DES.generate_key(passphrase, salt, key_length=16)  # 128-bit key for AES
    key_aes_192 = AES_DES.generate_key(passphrase, salt, key_length=24)  # 192-bit key for AES
    key_aes_256 = AES_DES.generate_key(passphrase, salt, key_length=32)  # 256-bit key for AES
    key_des = AES_DES.generate_key(passphrase, salt, key_length=8)       # 64-bit key for DES

    # Test AES encryption and decryption with different key sizes
    aes_des_aes = AES_DES(isAES=True)
    keys_aes = [key_aes_128, key_aes_192, key_aes_256]
    for key in keys_aes:
        encrypted_message_aes = aes_des_aes.encrypt_m(message, key)
        decrypted_message_aes = aes_des_aes.decrypt_m(encrypted_message_aes, key)
        assert decrypted_message_aes.decode() == message, f"AES encryption/decryption failed with key size {len(key)*8} bits"

    # Test DES encryption and decryption with different key sizes
    aes_des_des = AES_DES(isAES=False)
    encrypted_message_des = aes_des_des.encrypt_m(message, key_des)
    decrypted_message_des = aes_des_des.decrypt_m(encrypted_message_des, key_des)
    assert decrypted_message_des.decode() == message, "DES encryption/decryption failed"

    # Test encryption and decryption of empty message
    encrypted_empty_message_aes = aes_des_aes.encrypt_m(empty_message, key_aes_128)
    decrypted_empty_message_aes = aes_des_aes.decrypt_m(encrypted_empty_message_aes, key_aes_128)
    assert decrypted_empty_message_aes.decode() == empty_message, "Empty message encryption/decryption failed"

    # Test encryption and decryption of long message
    encrypted_long_message_aes = aes_des_aes.encrypt_m(long_message, key_aes_128)
    decrypted_long_message_aes = aes_des_aes.decrypt_m(encrypted_long_message_aes, key_aes_128)
    assert decrypted_long_message_aes.decode() == long_message, "Long message encryption/decryption failed"

    print("All AES and DES encryption/decryption tests passed!")

def main():
    test_aes_des()

if __name__ == "__main__":
    main()

