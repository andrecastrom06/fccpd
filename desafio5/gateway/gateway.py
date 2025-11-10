from flask import Flask, jsonify, Response
import requests
import os

app = Flask(__name__)

USERS_URL = os.getenv("USERS_URL", "http://service_users:5000/users")
ORDERS_URL = os.getenv("ORDERS_URL", "http://service_orders:5000/orders")

@app.route("/users")
def proxy_users():
    r = requests.get(USERS_URL, timeout=5)
    return Response(r.content, status=r.status_code, content_type=r.headers.get('Content-Type'))

@app.route("/orders")
def proxy_orders():
    r = requests.get(ORDERS_URL, timeout=5)
    return Response(r.content, status=r.status_code, content_type=r.headers.get('Content-Type'))

@app.route("/health")
def health():
    return jsonify({"status":"ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)