from Crypto.Cipher import AES, DES

def encrypt_aes(self, message, key):
    cipher = AES.new(key, AES.MODE_ECB)
    padded_message = self.pad_message(message)
    return cipher.encrypt(padded_message)

def decrypt_aes(self, message, key):
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted_message = cipher.decrypt(message)
    return self.unpad_message(decrypted_message)

def encrypt_des(self, message, key):
    cipher = DES.new(key, DES.MODE_ECB)
    padded_message = self.pad_message(message)
    return cipher.encrypt(padded_message)

def decrypt_des(self, message, key):
    cipher = DES.new(key, DES.MODE_ECB)
    decrypted_message = cipher.decrypt(message)
    return self.unpad_message(decrypted_message)

def pad_message(self, message):
    block_size = AES.block_size if self.isAES == "True" else DES.block_size
    padding_size = block_size - len(message) % block_size
    padding = bytes([padding_size] * padding_size)
    return message.encode() + padding

def unpad_message(self, message):
    padding_size = message[-1]
    return message[:-padding_size]