import random
from datetime import date, timedelta
import requests
import time

PRIVATE_CLOUD_URL = "http://127.0.0.1:5001/register"

FIRST_NAMES = [
    "Arun", "Meena", "Ravi", "Anita", "Karthik", "Priya",
    "Suresh", "Divya", "Rahul", "Sneha", "Vikram", "Asha"
]

def random_dob(min_age=18, max_age=65):
    today = date.today()
    age = random.randint(min_age, max_age)
    dob = today - timedelta(days=365 * age)
    return dob.isoformat()

def generate_users(start=1, count=10000, delay=0.01):
    print(f"Generating {count} synthetic users...\n")

    for i in range(start, start + count):
        payload = {
            "citizen_id": f"CIT{i:05d}",   # supports >10k cleanly
            "name": random.choice(FIRST_NAMES) + str(i),
            "dob": random_dob(),
            "is_student": random.choice([0, 1])
        }

        try:
            r = requests.post(PRIVATE_CLOUD_URL, json=payload)

            if r.status_code == 200:
                if i % 500 == 0:
                    print(f"[OK] Registered {i} users")
            else:
                print(f"[SKIP] {payload['citizen_id']}")

        except Exception as e:
            print(f"[ERROR] {payload['citizen_id']} → {e}")

        time.sleep(delay)

    print("\nDataset generation completed.")

if __name__ == "__main__":
    generate_users(count=10000)
