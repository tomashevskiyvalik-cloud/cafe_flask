from . import db
from datetime import datetime

class Tovar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nazva = db.Column(db.String(150), nullable=False)
    opis = db.Column(db.Text, nullable=False)
    tsina = db.Column(db.Float, nullable=False)

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tovar_id = db.Column(db.Integer, db.ForeignKey('tovar.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    tovar = db.relationship('Tovar', backref=db.backref('orders', lazy=True))
