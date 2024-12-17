
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os

class NaivePIR:
    def __init__(self, records):
        self.keys = [os.urandom(16) for _ in records]  # Unique AES keys per record
        self.records = [self.encrypt(record, key) for record, key in zip(records, self.keys)]

    def encrypt(self, record, key):
        """Encrypt a record using AES."""
        cipher = Cipher(algorithms.AES(key), modes.ECB())
        encryptor = cipher.encryptor()
        padded_record = record.ljust(32, b'\x00')  # Pad to 32 bytes
        return encryptor.update(padded_record) + encryptor.finalize()

    def decrypt(self, encrypted_record, key):
        """Decrypt a record using AES."""
        cipher = Cipher(algorithms.AES(key), modes.ECB())
        decryptor = cipher.decryptor()
        return decryptor.update(encrypted_record).rstrip(b'\x00')

    def query(self, index):
        """Client query: request an encrypted record and its key."""
        return self.records[index], self.keys[index]

    def verify(self, record, decrypted_record):
        """Verify the integrity of the decrypted record."""
        return record == decrypted_record
