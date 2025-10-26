import csv
import hashlib
def hash_password(password):
    # Hash password using SHA-256 (like HIBP)
    return hashlib.sha256(password.encode()).hexdigest().upper()
def load_breach_data():
    # Read breach data from CSV
    breaches = []
    with open("breach_data.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Store email and hashed password
            breaches.append({
                "email": row["email"],
                "password_hash": hash_password(row["password"])
            })
    return breaches
def check_breach(email, password):
    # Load breach data
    breach_data = load_breach_data()
    # Hash input password
    password_hash = hash_password(password)
    # Check if email or password is breached
    for breach in breach_data:
        if breach["email"] == email:
            print(f"WARNING: Email '{email}' found in breach!")
            return
        if breach["password_hash"] == password_hash:
            print(f"WARNING: Password '{password}' found in breach!")
            return
    print("No breach found. You're safe!")
# Get user input
user_email = input("Enter your email: ")
user_password = input("Enter your password: ")
# Check for breach
check_breach(user_email, user_password)