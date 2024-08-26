import pyotp

# Khóa bí mật Base32 của bạn
secret_key = 'AEIUZLAQWR7IFCJBA5KF24ERHIQUBOBN'

# Tạo đối tượng TOTP
totp = pyotp.TOTP(secret_key)

# Lấy mã xác thực hiện tại
current_otp = totp.now()

print("Mã xác thực hiện tại:", current_otp)
