from flask import Flask, request, jsonify
import jwt
from crypto_utils import decrypt_claim

app = Flask(__name__)

with open("keys/public.pem", "rb") as f:
    PUBLIC_KEY = f.read()

@app.route("/verify", methods=["POST"])
def verify_token():
    token = request.json.get("token")

    try:
        decoded = jwt.decode(
            token,
            PUBLIC_KEY,
            algorithms=["RS256"],
            audience="citizen-services"
        )

        claims = decoded["claims"]
        is_student = decrypt_claim(claims["isStudent"])

        if is_student == "true":
            return jsonify({"access": "GRANTED"})
        else:
            return jsonify({"access": "DENIED"})

    except Exception as e:
        return jsonify({"error": str(e)}), 401

if __name__ == "__main__":
    app.run(port=6000)
