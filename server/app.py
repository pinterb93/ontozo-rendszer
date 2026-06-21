import os
import mysql.connector
from flask import Flask, request, jsonify

app = Flask(__name__)

DB_CONFIG = {
    "host": os.environ.get("DB_HOST", "mariadb"),
    "port": int(os.environ.get("DB_PORT", 3306)),
    "user": os.environ.get("DB_USER", "ontozo_app"),
    "password": os.environ.get("DB_PASSWORD", ""),
    "database": os.environ.get("DB_NAME", "ontozo"),
}

API_TOKEN = os.environ.get("API_TOKEN", "")


def is_authorized(req):
    if not API_TOKEN:
        return False
    return req.headers.get("Authorization") == f"Bearer {API_TOKEN}"


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route("/api/v1/daily-moisture", methods=["POST"])
def save_daily_moisture():
    if not is_authorized(request):
        return jsonify({"error": "unauthorized"}), 401

    payload = request.get_json(silent=True)
    if not payload:
        return jsonify({"error": "invalid json body"}), 400

    device_uid = payload.get("device_uid")
    date = payload.get("date")
    avg_moisture = payload.get("avg_moisture")

    if not device_uid or not date or avg_moisture is None:
        return jsonify({"error": "device_uid, date and avg_moisture are required"}), 400

    try:
        avg_moisture = float(avg_moisture)
    except (TypeError, ValueError):
        return jsonify({"error": "avg_moisture must be numeric"}), 400

    if avg_moisture < 0 or avg_moisture > 100:
        return jsonify({"error": "avg_moisture must be between 0 and 100"}), 400

    conn = mysql.connector.connect(**DB_CONFIG)
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO daily_moisture (device_uid, date, avg_moisture)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE avg_moisture = %s
            """,
            (device_uid, date, avg_moisture, avg_moisture),
        )
        conn.commit()
    finally:
        cursor.close()
        conn.close()

    return jsonify({"status": "stored"}), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
