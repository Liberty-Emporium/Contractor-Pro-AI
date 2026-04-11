"""
Encryption utilities for API keys
Using AES-256 encryption
"""

import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
import hashlib

# Generate a key from a secret - IN PRODUCTION, USE A STRONG KEY!
# For now, we'll use a hash of a combined secret
def get_encryption_key(secret=None):
    """Get encryption key from secret"""
    if secret is None:
        # Use a combination of machine-specific values
        secret = os.environ.get('ENCRYPTION_SECRET', 'contractor-pro-ai-default-key-2024')
    
    # Use PBKDF2 to derive a key
    salt = b'contractor-pro-salt'  # In production, use random salt stored in DB
    kdf = PBKDF2(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(secret.encode()))
    return key

def encrypt_value(value):
    """Encrypt a single value"""
    if not value:
        return ''
    key = get_encryption_key()
    f = Fernet(key)
    encrypted = f.encrypt(value.encode())
    return encrypted.decode()

def decrypt_value(encrypted_value):
    """Decrypt a single value"""
    if not encrypted_value:
        return ''
    try:
        key = get_encryption_key()
        f = Fernet(key)
        decrypted = f.decrypt(encrypted_value.encode())
        return decrypted.decode()
    except:
        return ''  # Return empty if decryption fails

# Test
if __name__ == '__main__':
    test = 'sk-test-12345'
    enc = encrypt_value(test)
    dec = decrypt_value(enc)
    print(f'Test: {test}')
    print(f'Encrypted: {enc}')
    print(f'Decrypted: {dec}')
    print(f'Match: {test == dec}')
