from flask import Flask, jsonify
import requests

app = Flask(__name__)

SERVICE_A_URL = "http://service_a:5000/users"

@app.route("/")
def consume():
    try:
        res = requests.get(SERVICE_A_URL, timeout=2)
        users = res.json()

        formatted = [
            f"Usuario {u['name']} ativo desde {u['active_since']}"
            for u in users
        ]

        return jsonify(formatted)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6000)
