"""
Address Mirror — утилита для генерации Bitcoin-адресов, у которых начало и конец совпадают.
"""

import secrets
import base58
import hashlib
import ecdsa

def generate_keypair():
    private_key = secrets.token_bytes(32)
    sk = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1)
    vk = sk.verifying_key
    public_key = b'\x04' + vk.to_string()
    return private_key, public_key

def pubkey_to_address(public_key):
    sha256 = hashlib.sha256(public_key).digest()
    ripemd160 = hashlib.new('ripemd160', sha256).digest()
    prefix = b'\x00'
    payload = prefix + ripemd160
    checksum = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
    address = base58.b58encode(payload + checksum)
    return address.decode()

def is_mirror(address):
    return address[1:4] == address[-3:]

def find_mirror_address():
    attempts = 0
    while True:
        priv, pub = generate_keypair()
        addr = pubkey_to_address(pub)
        attempts += 1
        if is_mirror(addr):
            print(f"🔑 Приватный ключ: {priv.hex()}")
            print(f"🏦 Адрес: {addr}")
            print(f"🔁 Попыток: {attempts}")
            break

if __name__ == "__main__":
    print("🚀 Ищем зеркальный адрес (начало и конец совпадают)...")
    find_mirror_address()
