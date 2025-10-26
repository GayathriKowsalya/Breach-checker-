from flask import Flask, render_template, request
import csv
import hashlib

app = Flask(__name__)

def hash_password(password):
    # Hash password using SHA-256
    return hashlib.sha256(password.encode()).hexdigest().upper()

def load_breach_data():
    # Read breach data from CSV
    breaches = []
    try:
        with open("breach_data.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                breaches.append({
                    "email": row["email"],
                    "password_hash": hash_password(row["password"])
                })
    except FileNotFoundError:
        return []
    return breaches

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        password_hash = hash_password(password)
        breach_data = load_breach_data()
        
        for breach in breach_data:
            if breach["email"] == email:
                result = f"WARNING: Email '{email}' found in breach!"
                break
            if breach["password_hash"] == password_hash:
                result = f"WARNING: Password found in breach!"
                break
        if not result:
            result = "No breach found. You're safe!"
    
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)