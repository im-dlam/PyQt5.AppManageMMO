import pyotp

def Authentication(secret_key):
    totp = pyotp.TOTP(secret_key)
    current_otp = totp.now()
    return str(current_otp)