"""
Helper script to reset a user's password
Usage: python reset_password.py <username> <new_password>
"""
import sys
from app.database import engine
from app.auth import get_password_hash
from sqlalchemy import text

if len(sys.argv) != 3:
    print("Usage: python reset_password.py <username> <new_password>")
    print("\nExample: python reset_password.py demo_user mypassword123")
    sys.exit(1)

username = sys.argv[1]
new_password = sys.argv[2]

with engine.begin() as conn:
    # Check if user exists
    result = conn.execute(
        text("SELECT id FROM users WHERE username = :username"),
        {"username": username}
    ).fetchone()
    
    if not result:
        print(f"❌ User '{username}' not found!")
        print("\nAvailable users:")
        users = conn.execute(text("SELECT username FROM users")).fetchall()
        for user in users:
            print(f"  - {user[0]}")
        sys.exit(1)
    
    # Update password
    hashed_password = get_password_hash(new_password)
    conn.execute(
        text("UPDATE users SET hashed_password = :hashed_password WHERE username = :username"),
        {"hashed_password": hashed_password, "username": username}
    )
    
    print(f"✅ Password reset successful!")
    print(f"Username: {username}")
    print(f"New Password: {new_password}")
    print(f"\nYou can now login with these credentials.")
