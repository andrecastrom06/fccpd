from flask import Flask, request
import logging
app = Flask(__name__)

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')

@app.route("/")
def index():
    app.logger.info(f"Request recebido de {request.remote_addr}")
    return "OK from server", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
