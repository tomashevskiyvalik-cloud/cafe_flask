import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from sqlalchemy import text

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # SECRET KEY з ENV
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')

    # SQLite шлях з ENV (Docker volume)
    database_path = os.environ.get('DATABASE_PATH', 'cafe.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{database_path}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    CORS(app)

    db.init_app(app)
    Migrate(app, db)

    # ✅ ВАЖЛИВО: імпортуємо моделі, щоб SQLAlchemy “побачив” таблиці
    from .models import Tovar, Feedback, Order  # noqa: F401

    # ✅ Створюємо таблиці, якщо їх ще нема (для нової SQLite бази)
    with app.app_context():
        db.create_all()

    # Healthcheck endpoint (SQLAlchemy 2.x compatible)
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