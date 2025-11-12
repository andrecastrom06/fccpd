from flask import Flask
import psycopg2
import redis

app = Flask(__name__)

@app.route("/")
def index():
    try:
        conn = psycopg2.connect(
            host="db",
            user="user",
            password="pass",
            dbname="teste",
        )
        db_status = "OK"
        conn.close()
    except Exception as e:
        db_status = f"ERRO: {e}"

    try:
        r = redis.Redis(host="cache", port=6379)
        r.set("ping", "pong")
        cache_status = r.get("ping").decode()
    except Exception as e:
        cache_status = f"ERRO: {e}"

    return {
        "db": db_status,
        "cache": cache_status
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)