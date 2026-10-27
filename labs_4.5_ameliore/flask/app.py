import os

import psycopg2
import requests
from flask import Flask, jsonify
from redis import Redis

app = Flask(__name__)

redis = Redis(host=os.getenv("REDIS_HOST", "localhost"), port=6379, decode_responses=True)
SPRING_URL = os.getenv("SPRING_URL", "http://localhost:8080")
PG_PARAMS = dict(
    host=os.getenv("POSTGRES_HOST", "localhost"),
    port=5432,
    user=os.getenv("POSTGRES_USER", "postgres"),
    password=os.getenv("POSTGRES_PASSWORD", "postgres"),
    dbname=os.getenv("POSTGRES_DB", "postgres"),
)


def postgres_version():
    with psycopg2.connect(**PG_PARAMS) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            return cursor.fetchone()[0]


@app.route("/")
def index():
    result = {"flask": "Hello, Flask!"}
    # Redis : compteur de visites
    try:
        result["hits"] = redis.incr("flask_hits")
    except Exception as error:
        result["hits"] = f"ERREUR Redis : {error}"
    # PostgreSQL : version du serveur
    try:
        result["postgres"] = postgres_version()
    except Exception as error:
        result["postgres"] = f"ERREUR PostgreSQL : {error}"
    # Spring Boot : appel HTTP
    try:
        result["spring"] = requests.get(SPRING_URL, timeout=5).text
    except Exception as error:
        result["spring"] = f"ERREUR Spring Boot : {error}"
    return jsonify(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
