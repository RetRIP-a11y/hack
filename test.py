from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from Crypto.Random import new as Random
from base64 import b64encode
from base64 import b64decode


def generate_key(key_length):
    assert key_length in [1024, 2048, 4096]
    rng = Random().read
    key = RSA.generate(key_length, rng)
    return key


def encrypt(data, key):
    plaintext = b64encode(data.encode())
    rsa_encryption_cipher = PKCS1_v1_5.new(key)
    ciphertext = rsa_encryption_cipher.encrypt(plaintext)
    return b64encode(ciphertext).decode()


def decrypt(data, key):
    ciphertext = b64decode(data.encode())
    rsa_decryption_cipher = PKCS1_v1_5.new(key)
    plaintext = rsa_decryption_cipher.decrypt(ciphertext, 16)
    return b64decode(plaintext).decode()


key = generate_key(1024)
a = encrypt('Иванов И.И.', key)
# key = generate_key(1024)
b = decrypt(a, key)
print(a, b, sep='\n')
print('\n'*3)
print(key)