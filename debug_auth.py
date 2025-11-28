from app.utils import hash_password

try:
    print("Attempting to hash password...")
    hashed = hash_password("testpassword")
    print(f"Success: {hashed}")
except Exception as e:
    print(f"Error: {e}")
