from flask import Blueprint, jsonify, request
from .models import Tovar, Order, Feedback
from . import db

api = Blueprint("api", __name__, url_prefix="/api")

# ================== TOVAR ==================

@api.route("/tovars", methods=["GET"])
def get_tovars():
    tovars = Tovar.query.all()
    return jsonify([t.to_dict() for t in tovars])

@api.route("/tovars/<int:id>", methods=["GET"])
def get_tovar(id):
    tovar = Tovar.query.get_or_404(id)
    return jsonify(tovar.to_dict())

@api.route("/tovars", methods=["POST"])
def create_tovar():
    data = request.get_json()
    tovar = Tovar(
        nazva=data["nazva"],
        opis=data["opis"],
        tsina=data["tsina"]
    )
    db.session.add(tovar)
    db.session.commit()
    return jsonify(tovar.to_dict()), 201

@api.route("/tovars/<int:id>", methods=["PUT"])
def update_tovar(id):
    tovar = Tovar.query.get_or_404(id)
    data = request.get_json()

    tovar.nazva = data.get("nazva", tovar.nazva)
    tovar.opis = data.get("opis", tovar.opis)
    tovar.tsina = data.get("tsina", tovar.tsina)

    db.session.commit()
    return jsonify(tovar.to_dict())

@api.route("/tovars/<int:id>", methods=["DELETE"])
def delete_tovar(id):
    tovar = Tovar.query.get_or_404(id)
    db.session.delete(tovar)
    db.session.commit()
    return jsonify({"deleted": True})


# ================== ORDERS ==================

@api.route("/orders", methods=["GET"])
def get_orders():
    orders = Order.query.all()
    return jsonify([o.to_dict() for o in orders])

@api.route("/orders", methods=["POST"])
def create_order():
    data = request.get_json()
    order = Order(
        tovar_id=data["tovar_id"],
        name=data["name"],
        phone=data["phone"],
        quantity=data.get("quantity", 1)
    )
    db.session.add(order)
    db.session.commit()
    return jsonify(order.to_dict()), 201


# ================== FEEDBACK ==================

@api.route("/feedbacks", methods=["GET"])
def get_feedbacks():
    feedbacks = Feedback.query.all()
    return jsonify([f.to_dict() for f in feedbacks])

@api.route("/feedbacks", methods=["POST"])
def create_feedback():
    data = request.get_json()
    feedback = Feedback(
        name=data["name"],
        email=data["email"],
        message=data["message"]
    )
    db.session.add(feedback)
    db.session.commit()
    return jsonify(feedback.to_dict()), 201