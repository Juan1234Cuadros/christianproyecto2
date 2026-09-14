import os
import pymysql
from flask import Flask, jsonify

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "appdb")


def get_db_connection():
    return pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        connect_timeout=5,
    )


@app.route("/")
def index():
    """
    Ruta principal: se conecta de verdad a MySQL y ejecuta una consulta.
    Si la base de datos cae, esto lanza una excepción de PyMySQL
    (OperationalError) que Flask propaga como error 500, y que queda
    registrada en los logs del contenedor (visible en Dozzle).
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        return jsonify({"status": "ok", "db": "connected"}), 200
    finally:
        conn.close()


@app.route("/health")
def health():
    """Health check simple, sin tocar la base de datos."""
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
