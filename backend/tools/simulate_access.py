import requests
import time

UNIFIED_BACKEND_URL = "http://127.0.0.1:7000/access-service"

def simulate_access(citizen_id, service, device_id):
    payload = {
        "citizen_id": citizen_id,
        "name": "NA",               # ignored for old users
        "dob": "2000-01-01",        # ignored for old users
        "is_student": 1,
        "service": service,
        "device_id": device_id
    }

    response = requests.post(UNIFIED_BACKEND_URL, json=payload)

    if response.status_code == 200:
        result = response.json()
        print(f"{citizen_id} → {result['access']}")
    else:
        print(f"{citizen_id} → ERROR")

if __name__ == "__main__":
    print("Simulating access for old users...\n")

    for i in range(1, 11):
        cid = f"CIT{i:04d}"
        simulate_access(cid, "education", "DEVICE-EDU-01")
        time.sleep(0.3)
