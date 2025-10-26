import requests
import hashlib

# Placeholder for HIBP API key
HIBP_API_KEY = "YOUR_API_KEY_HERE"  # Replace with your HIBP API key

# Check if password is in Pwned Passwords via API
def check_pwned_api(password):
    sha1 = hashlib.sha1(password.encode()).hexdigest().upper()
    prefix, suffix = sha1[:5], sha1[5:]
    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    headers = {"api-key": HIBP_API_KEY} if HIBP_API_KEY != "YOUR_API_KEY_HERE" else {}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            hashes = response.text.splitlines()
            for h in hashes:
                if h.startswith(suffix):
                    count = int(h.split(':')[1])
                    return count > 0, count
        return False, 0
    except Exception as e:
        print(f"API error: {e}")
        return False, 0

# Optional: Check local Pwned Passwords subset (if you keep pwned_subset.txt)
def load_pwned_passwords(pwned_path):
    pwned_dict = {}
    try:
        with open(pwned_path, 'r') as f:
            for line in f:
                suffix, count = line.strip().split(':')
                pwned_dict[suffix] = int(count)
        return pwned_dict
    except FileNotFoundError:
        print(f"Local Pwned Passwords file ({pwned_path}) not found. Relying on API.")
        return {}

def is_pwned_password(password, pwned_dict):
    if not pwned_dict:  # If local file is missing or not used
        return False, 0
    sha1 = hashlib.sha1(password.encode()).hexdigest().upper()
    suffix = sha1[5:]
    count = pwned_dict.get(suffix, 0)
    return count > 0, count

# Main password checker
def check_password(password, pwned_dict=None):
    # Check via HIBP API
    is_pwned, breach_count = check_pwned_api(password)
    if is_pwned:
        return f"Password '{password}' was found in a data breach ({breach_count} occurrences). Change it!"

    # Optional: Check local Pwned Passwords subset (if provided)
    if pwned_dict:
        is_pwned_local, local_count = is_pwned_password(password, pwned_dict)
        if is_pwned_local:
            return f"Password '{password}' was found in a data breach (local data, {local_count} occurrences). Change it!"

    # Basic length check (optional, customize as needed)
    if len(password) < 8:
        return f"Password '{password}' is too short. Use at least 8 characters."

    return f"Password '{password}' seems safe!"

# Load local Pwned Passwords (optional, comment out if not needed)
pwned_dict = load_pwned_passwords('pwned_subset.txt')  # Remove if you don’t want local checks

# Example usage
if __name__ == "__main__":
    test_passwords = ["password", "123456", "SecurePass123", "randomtext"]
    for pwd in test_passwords:
        print(check_password(pwd, pwned_dict))