import requests

BASE = "http://127.0.0.1:7000"

# 1. REGISTER USER
res = requests.post(BASE + "/register-user", json={
    "username": "testuser",
    "password": "1234"
})
print("REGISTER:", res.json())

# 2. LOGIN USER
res = requests.post(BASE + "/login-user", json={
    "username": "testuser",
    "password": "1234"
})
print("LOGIN:", res.json())