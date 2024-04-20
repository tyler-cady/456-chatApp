import os
from Crypto.Cipher import AES, DES
from Crypto.Util.Padding import pad, unpad

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
            return unpad(decrypted_message, AES.block_size)
        else:
            cipher = DES.new(key, DES.MODE_ECB)
            decrypted_message = cipher.decrypt(message)
            return unpad(decrypted_message, DES.block_size)

    def pad_message(self, message):
        block_size = AES.block_size if self.isAES else DES.block_size
        padding_size = block_size - len(message) % block_size
        padding = bytes([padding_size] * padding_size)
        return message.encode() + padding

    def unpad_message(self, message):
        padding_size = message[-1]
        return message[:-padding_size]