from faker import Faker
import csv
fake = Faker()
# Create 10 fake "breached" records
data = []
for _ in range(100000):
    email = fake.email()
    password = fake.password(length=8)
    data.append({"email": email, "password": password})
# Save to a CSV file
with open("breach_data.csv", "w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=["email", "password"])
    writer.writeheader()
    for row in data:
        writer.writerow(row)
print("Dataset created: breach_data.csv")