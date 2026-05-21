from flask import Flask, request, jsonify
import requests
from datetime import datetime
from private_cloud.crypto import generate_duid, encrypt_value, hash_metadata
from private_cloud.storage import init_private_db, store_user, get_derived_attributes
from private_cloud.config import SYSTEM_SALT, TOKEN_EXPIRY_SECONDS
from shared.token_utils import issue_jwt

app = Flask(__name__)
init_private_db()



@app.route("/register", methods=["POST"])
def register_user():
    data = request.json

    citizen_id = data["citizen_id"]
    name = data["name"]
    dob = data["dob"]
    is_student = int(data["is_student"])

    duid = generate_duid(citizen_id, SYSTEM_SALT)
    year = int(dob.split("-")[0])
    current_year = datetime.now().year
    age = current_year - year
    is_adult = 1 if age >= 18 else 0
    is_health_eligible = 1 if age >= 60 else 0

    print("AGE:", age)
    print("ADULT:", is_adult)
    print("HEALTH:", is_health_eligible)

    store_user(
        duid,
        encrypt_value(name),
        encrypt_value(dob),
        is_adult,
        is_student,
        is_health_eligible
    )

    return jsonify({
        "message": "User registered securely",
        "duid": duid
    })



@app.route("/issue-token", methods=["POST"])
def issue_token():
    data = request.json

    citizen_id = data["citizen_id"]
    service = data["service"]
    device_id = data["device_id"]

    duid = generate_duid(citizen_id, SYSTEM_SALT)
    attrs = get_derived_attributes(duid)

    if not attrs:
        return jsonify({"error": "User not found"}), 404

    is_adult, is_student, is_health_eligible = attrs

    claims = {
        "isAdult": encrypt_value(str(is_adult)),
        "isStudent": encrypt_value(str(is_student)),
        "isHealthEligible": encrypt_value(str(is_health_eligible))
    }

    payload = {
        "iss": "private-identity-hub",
        "sub": duid,
        "aud": "public-services",
        "claims": claims,
        "meta": {
            "service": service,
            "device": hash_metadata(device_id)
        }
    }

    token = issue_jwt(payload, TOKEN_EXPIRY_SECONDS)

    return jsonify({"token": token})



@app.route("/access-service", methods=["POST"])
def access_service():
    data = request.json

    citizen_id = data["citizen_id"]
    service = data["service"]
    device_id = data["device_id"]

    
    duid = generate_duid(citizen_id, SYSTEM_SALT)
    attrs = get_derived_attributes(duid)

    if not attrs:
        return jsonify({"error": "User not found"}), 404

    is_adult, is_student, is_health_eligible = attrs

    claims = {
        "isAdult": encrypt_value(str(is_adult)),
        "isStudent": encrypt_value(str(is_student)),
        "isHealthEligible": encrypt_value(str(is_health_eligible))
    }

    payload = {
        "iss": "private-identity-hub",
        "sub": duid,
        "aud": "public-services",
        "claims": claims,
        "meta": {
            "service": service,
            "device": hash_metadata(device_id)
        }
    }

    token = issue_jwt(payload, TOKEN_EXPIRY_SECONDS)


    public_url = "https://identity-hub-public.onrender.com/access-service"

    response = requests.post(
        public_url,
        json={
            "token": token,
            "device_hash": hash_metadata(device_id),
            "service": service
        }
    )

    return jsonify({
        "public_response": response.json()
    })



@app.route("/privacy-metric", methods=["GET"])
def privacy_metric():
    stored_attributes = 6
    disclosed_attributes = 1

    disclosure_ratio = disclosed_attributes / stored_attributes

    return {
        "stored_attributes": stored_attributes,
        "disclosed_attributes_per_service": disclosed_attributes,
        "disclosure_ratio": round(disclosure_ratio, 2)
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)