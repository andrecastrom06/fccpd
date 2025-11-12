from flask import Flask, jsonify
import psycopg2
import redis

app = Flask(__name__)

@app.route("/")
def index():
    result = {}

    try:
        conn = psycopg2.connect(
            host="db",
            user="user",
            password="pass",
            dbname="teste",
        )
        result["db"] = "OK"
        conn.close()
    except Exception as e:
        result["db"] = f"ERRO: {e}"

    try:
        r = redis.Redis(host="cache", port=6379)
        r.set("ping", "pong")
        result["cache"] = r.get("ping").decode()
    except Exception as e:
        result["cache"] = f"ERRO: {e}"

    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)