import secrets


def generate_otp(length: int = 6) -> str:
    max_val = 10**length
    return str(secrets.randbelow(max_val)).zfill(length)
