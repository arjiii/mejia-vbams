import sqlite3

# Connect to the database
conn = sqlite3.connect('vbams.db')
cursor = conn.cursor()

# Check if users table exists
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables:", tables)

# Check if the driver user exists
cursor.execute("SELECT id, email, role, hashed_password FROM users WHERE email='driver@test.com';")
user = cursor.fetchone()
if user:
    print("\nDriver user found:")
    print(f"  ID: {user[0]}")
    print(f"  Email: {user[1]}")
    print(f"  Role: {user[2]}")
    print(f"  Has password: {bool(user[3])}")
else:
    print("\nDriver user NOT found!")

conn.close()
