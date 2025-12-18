import os
import sqlite3

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from sqlalchemy import text, event
from sqlalchemy.engine import Engine

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    # SECRET KEY з ENV
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')

    # SQLite шлях з ENV (Docker volume)
    database_path = os.environ.get('DATABASE_PATH', 'cafe.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{database_path}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # ✅ Обмеження розміру upload (2MB)
    app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024

    CORS(app)

    db.init_app(app)
    Migrate(app, db)

    # ✅ Вмикаємо foreign keys для SQLite (щоб CASCADE працював)
    @event.listens_for(Engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        if isinstance(dbapi_connection, sqlite3.Connection):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON;")
            cursor.close()

    # ✅ Імпортуємо моделі
    from .models import Tovar, Feedback, Order  # noqa: F401

    # ✅ Створюємо таблиці, якщо їх ще нема + авто-мікро-міграція для SQLite
    with app.app_context():
        db.create_all()

        # Друк шляху до реально використаної БД (дуже корисно при дебазі)
        try:
            print("✅ DB path:", database_path)
        except Exception:
            pass

        # ✅ Додаємо колонку status, якщо база стара і в таблиці її нема
        def _ensure_status_column(table_name: str) -> bool:
            cols = db.session.execute(text(f'PRAGMA table_info("{table_name}");')).fetchall()
            if not cols:
                return False  # таблиці нема
            col_names = {c[1] for c in cols}  # c[1] = назва колонки
            if "status" not in col_names:
                db.session.execute(
                    text(f'ALTER TABLE "{table_name}" ADD COLUMN status VARCHAR(20) NOT NULL DEFAULT "NEW";')
                )
                db.session.commit()
            return True

        try:
            # пробуємо "order"
            if not _ensure_status_column("order"):
                # якщо таблиця називається orders
                _ensure_status_column("orders")
        except Exception:
            # не валимо застосунок через міграцію
            pass

    @app.get("/health")
    def health():
        try:
            db.session.execute(text("SELECT 1"))
            return jsonify(status="ok", db="connected"), 200
        except Exception as e:
            return jsonify(status="error", detail=str(e)), 500

    from .routes import main_bp
    from .admin_routes import admin_bp
    from .api import api

    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(api)

    return app