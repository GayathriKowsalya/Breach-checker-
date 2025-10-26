import sqlite3
import csv
import hashlib

def hash_password_sha1(password):
    return hashlib.sha1(password.encode()).hexdigest().upper()

def get_k_anon_prefix(hash_str):
    return hash_str[:5]

# Connect to SQLite database
conn = sqlite3.connect("breach.db")
cursor = conn.cursor()

# Create tables
cursor.execute("""
    CREATE TABLE IF NOT EXISTS emails (
        email TEXT PRIMARY KEY
    )
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS passwords (
        prefix TEXT,
        full_hash TEXT,
        PRIMARY KEY (prefix, full_hash)
    )
""")

# Load breach_data.csv (emails)
try:
    with open("breach_data.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            cursor.execute("INSERT OR IGNORE INTO emails (email) VALUES (?)", (row["email"],))
except FileNotFoundError:
    print("breach_data.csv not found")

# Load pwned_passwords_subset.txt (passwords)
try:
    with open("pwned_passwords_subset.txt", "r") as file:
        for line in file:
            try:
                hash_val, _ = line.strip().split(":")
                prefix = get_k_anon_prefix(hash_val)
                cursor.execute("INSERT OR IGNORE INTO passwords (prefix, full_hash) VALUES (?, ?)", (prefix, hash_val))
            except ValueError:
                continue
except FileNotFoundError:
    print("pwned_passwords_subset.txt not found")

# Commit and close
conn.commit()
conn.close()
print("Database created: breach.db")