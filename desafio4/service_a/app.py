from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/users")
def users():
    return jsonify([
        {"id": 1, "name": "Andre", "active_since": "2006"},
        {"id": 2, "name": "Jorge", "active_since": "2025"},
        {"id": 3, "name": "Cesar", "active_since": "2023"}
    ])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)