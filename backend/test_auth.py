from app.database import engine
from app.auth import verify_password, get_password_hash
from sqlalchemy import text

# Check users in database
with engine.connect() as conn:
    users = conn.execute(text('SELECT id, username, hashed_password FROM users')).fetchall()
    print(f"\n=== Users in Database ===")
    for user in users:
        print(f"ID: {user[0]}, Username: {user[1]}")
        print(f"Hashed Password: {user[2][:50]}...")
    
    if not users:
        print("No users found in database")

# Test password hashing and verification
print(f"\n=== Testing Password Hash ===")
test_password = "test123"
hashed = get_password_hash(test_password)
print(f"Original password: {test_password}")
print(f"Hashed: {hashed[:50]}...")
print(f"Verification result: {verify_password(test_password, hashed)}")

# Test with actual user if exists
if users:
    print(f"\n=== Testing User Password ===")
    test_user = users[0]
    print(f"Testing user: {test_user[1]}")
    # Try common test passwords
    for pwd in ["test", "test123", "password", "admin"]:
        result = verify_password(pwd, test_user[2])
        if result:
            print(f"✓ Password '{pwd}' works!")
        else:
            print(f"✗ Password '{pwd}' doesn't match")
