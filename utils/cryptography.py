from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import base64

class Cryptography:
    KEY = b"rengina!@#$%^&*"

    @staticmethod
    def encrypt(to_encrypt: str, use_hashing: bool = True) -> str:
        try:
            key = Cryptography.KEY
            if use_hashing:
                digest = hashes.Hash(hashes.MD5(), backend=default_backend())
                digest.update(key)
                key = digest.finalize()

            cipher = Cipher(algorithms.TripleDES(key), modes.ECB(), backend=default_backend())
            encryptor = cipher.encryptor()

            padded_data = Cryptography._pad(to_encrypt.encode('utf-8'))
            encrypted = encryptor.update(padded_data) + encryptor.finalize()
            return base64.b64encode(encrypted).decode('utf-8')
        except Exception as ex:
            return str(ex)

    @staticmethod
    def decrypt(cipher_string: str, use_hashing: bool = True) -> str:
        try:
            key = Cryptography.KEY
            if use_hashing:
                digest = hashes.Hash(hashes.MD5(), backend=default_backend())
                digest.update(key)
                key = digest.finalize()

            cipher = Cipher(algorithms.TripleDES(key), modes.ECB(), backend=default_backend())
            decryptor = cipher.decryptor()

            encrypted_data = base64.b64decode(cipher_string)
            decrypted = decryptor.update(encrypted_data) + decryptor.finalize()
            return Cryptography._unpad(decrypted).decode('utf-8')
        except Exception as ex:
            return str(ex)

    @staticmethod
    def _pad(data: bytes, block_size: int = 8) -> bytes:
        padding_length = block_size - len(data) % block_size
        return data + bytes([padding_length] * padding_length)

    @staticmethod
    def _unpad(data: bytes) -> bytes:
        padding_length = data[-1]
        return data[:-padding_length]