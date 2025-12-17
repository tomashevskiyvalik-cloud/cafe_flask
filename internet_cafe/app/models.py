from . import db
from datetime import datetime


class Tovar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nazva = db.Column(db.String(150), nullable=False)
    opis = db.Column(db.Text, nullable=False)
    tsina = db.Column(db.Float, nullable=False)

    # ✅ НОВЕ ПОЛЕ ДЛЯ ФОТО (назва файлу в static/uploads/tovary/)
    image_filename = db.Column(db.String(255), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "nazva": self.nazva,
            "opis": self.opis,
            "tsina": self.tsina,
            "image_filename": self.image_filename
        }


class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "message": self.message,
            "created_at": self.created_at.isoformat()
        }


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tovar_id = db.Column(db.Integer, db.ForeignKey('tovar.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    tovar = db.relationship('Tovar', backref=db.backref('orders', lazy=True))

    def to_dict(self):
        return {
            "id": self.id,
            "tovar_id": self.tovar_id,
            "tovar_nazva": self.tovar.nazva,
            "quantity": self.quantity,
            "name": self.name,
            "phone": self.phone,
            "created_at": self.created_at.isoformat()
        }