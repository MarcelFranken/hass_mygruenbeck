import random
import string
import hashlib
import base64

def generate_code_verifier() -> str:
    code_verifier_length = 64
    chars = string.ascii_letters + string.digits
    code_verifier = ''.join(random.choice(chars) for _ in range(code_verifier_length))
    return code_verifier

def generate_code_challenge(code_verifier: str) -> str:
    sha256_code_verifier = hashlib.sha256(code_verifier.encode()).digest()
    code_challenge = base64.urlsafe_b64encode(sha256_code_verifier).rstrip(b'=').decode()
    return code_challenge
