import os
import socket

import redis
from flask import Flask, jsonify

app = Flask(__name__)

# "db" — ім'я сервісу; його IP повертає вбудований DNS Docker (127.0.0.11).
r = redis.Redis(
    host=os.getenv("DB_HOST", "db"),
    port=int(os.getenv("DB_PORT", "6379")),
    socket_connect_timeout=2,
)


@app.get("/")
def index():
    try:
        visits = r.incr("visits")
    except redis.RedisError as e:
        # Якщо БД недоступна, повертаємо 503 у JSON замість типової HTML-сторінки 500.
        return jsonify(service="app", container=socket.gethostname(),
                       error=f"db unavailable: {e}"), 503
    return jsonify(
        service="app",
        container=socket.gethostname(),  # ID контейнера: видно, яка репліка відповіла
        visits=visits,
    )


@app.get("/health")
def health():
    try:
        r.ping()
        return {"status": "ok"}, 200
    except redis.RedisError as e:
        return {"status": "db-unreachable", "error": str(e)}, 503
