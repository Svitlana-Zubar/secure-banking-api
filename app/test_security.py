from app.security import hash_password, verify_password

hashed = hash_password("TestOne123")

print(verify_password("TestOne123", hashed))
print(verify_password("TestWrong123", hashed))