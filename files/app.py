from flask import Flask, jsonify
import psycopg2
import socket
import os

app = Flask(__name__)

DB_HOST = os.environ.get("DB_HOST", "db")
DB_NAME = os.environ.get("DB_NAME", "pulsecheck")
DB_USER = os.environ.get("DB_USER", "pulsecheck_app")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "")


def get_db_connection():
    return psycopg2.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD)


def increment_and_get_counter():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS visits (id SERIAL PRIMARY KEY, count INTEGER NOT NULL DEFAULT 0)")
    cur.execute("SELECT id, count FROM visits LIMIT 1")
    row = cur.fetchone()
    if row is None:
        cur.execute("INSERT INTO visits (count) VALUES (1) RETURNING count")
        count = cur.fetchone()[0]
    else:
        row_id = row[0]
        cur.execute("UPDATE visits SET count = count + 1 WHERE id = %s RETURNING count", (row_id,))
        count = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return count


@app.route("/")
def index():
    count = increment_and_get_counter()
    return jsonify({
        "message": f"Hello from {socket.gethostname()}",
        "hostname": socket.gethostname(),
        "visit_count": count,
        "version": "1.1",
    })


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
