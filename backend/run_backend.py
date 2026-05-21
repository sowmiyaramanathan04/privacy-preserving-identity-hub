import sqlite3

def init_user_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users(
        username TEXT PRIMARY KEY,
        password BLOB
    )
    """)

    conn.commit()
    conn.close()

init_user_db()

from flask import Flask, request, jsonify
from private_cloud.crypto import hash_metadata
import requests
import bcrypt
from flask_cors import CORS




app = Flask(__name__)
CORS(app)

PRIVATE_BASE = "http://127.0.0.1:5001"
PUBLIC_BASE = "https://identity-hub-public.onrender.com"   # keep this

@app.route("/register-user", methods=["POST"])
def register_user():
    data = request.json
    username = data["username"]
    password = data["password"]

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    try:
        c.execute("INSERT INTO users VALUES (?,?)", (username, hashed))
        conn.commit()
        return {"status": "registered"}
    except:
        return {"status": "exists"}

@app.route("/login-user", methods=["POST"])
def login_user():
    data = request.json
    username = data["username"]
    password = data["password"]

    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute("SELECT password FROM users WHERE username=?", (username,))
    result = c.fetchone()

    if result:
        stored_hash = result[0]

        if bcrypt.checkpw(password.encode(), stored_hash):
            return {"status": "success"}

    return {"status": "fail"}

@app.route("/access-service", methods=["POST"])
def access_service():
    data = request.json

    try:

        citizen_payload = {
            "citizen_id": data["citizen_id"],
            "name": data["name"],
            "dob": data["dob"],
            "is_student": data["is_student"]
        }

        service = data["service"]
        device_id = data.get("device_id", "FIXED-DEVICE-01")

        # REGISTER USER IN PRIVATE CLOUD
        register_response = requests.post(
            f"{PRIVATE_BASE}/register",
            json=citizen_payload,
            timeout=60
        )

        print("REGISTER STATUS:", register_response.status_code)
        print("REGISTER RESPONSE:", register_response.text)

        # ISSUE TOKEN
        token_response = requests.post(
            f"{PRIVATE_BASE}/issue-token",
            json={
                "citizen_id": data["citizen_id"],
                "service": service,
                "device_id": device_id
            },
            timeout=60
        )

        print("TOKEN STATUS:", token_response.status_code)
        print("TOKEN RESPONSE:", token_response.text)

        if token_response.status_code != 200:
            return jsonify({
                "RESULT": "DENIED",
                "ERROR": "Token generation failed"
            })

        token = token_response.json().get("token")

        if not token:
            return jsonify({
                "RESULT": "DENIED",
                "ERROR": "No token received"
            })

        print("CALLING PUBLIC CLOUD...")

        try:
            access_response = requests.post(
                f"{PUBLIC_BASE}/access-service",
                json={
                    "token": token,
                    "device_hash": hash_metadata(device_id),
                    "service": service
                },
                timeout=60
            )

            print("PUBLIC STATUS:", access_response.status_code)
            print("PUBLIC RESPONSE:", access_response.text)

            if access_response.status_code != 200:
                raise Exception("Public service error")

            result = access_response.json()

            print("FINAL DECISION FROM PUBLIC:", result)

            decision = result.get("access", "DENIED")

        except Exception as e:
            print("PUBLIC CLOUD FAILED:", str(e))
            decision = "DENIED"

        print("PUBLIC CLOUD RESPONDED")

        return jsonify({
            "RESULT": decision,
            "SERVICE": service,
            "FLOW": "Private → Public → Policy Engine",
            "SECURITY": {
                "Token": "RS256 Signed JWT",
                "Encryption": "AES-256",
                "Device Binding": "Enabled",
                "Identity Exposure": "None (DUID used)"
            }
        })

    except Exception as e:
        print("ERROR:", str(e))

        return jsonify({
            "RESULT": "DENIED",
            "ERROR": "System failure"
        })

if __name__ == "__main__":
    app.run(port=7000)