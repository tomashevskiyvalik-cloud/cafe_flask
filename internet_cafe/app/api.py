from flask import Blueprint, jsonify, request
from .models import Tovar, Order, Feedback
from . import db

api = Blueprint("api", __name__, url_prefix="/api")


# ================== TOVAR ==================

@api.get("/tovars")
def get_tovars():
    tovars = Tovar.query.order_by(Tovar.id.desc()).all()
    return jsonify([t.to_dict() for t in tovars])


@api.get("/tovars/<int:id>")
def get_tovar(id):
    tovar = Tovar.query.get_or_404(id)
    return jsonify(tovar.to_dict())


@api.post("/tovars")
def create_tovar():
    data = request.get_json(silent=True) or {}

    nazva = (data.get("nazva") or "").strip()
    opis = (data.get("opis") or "").strip()
    tsina = data.get("tsina", None)

    if not nazva or not opis or tsina is None:
        return jsonify(error="nazva/opis/tsina required"), 400

    try:
        tsina = float(tsina)
    except Exception:
        return jsonify(error="tsina must be a number"), 400

    tovar = Tovar(nazva=nazva, opis=opis, tsina=tsina)
    db.session.add(tovar)
    db.session.commit()
    return jsonify(tovar.to_dict()), 201


@api.put("/tovars/<int:id>")
def update_tovar(id):
    tovar = Tovar.query.get_or_404(id)
    data = request.get_json(silent=True) or {}

    if "nazva" in data:
        tovar.nazva = (data.get("nazva") or "").strip() or tovar.nazva
    if "opis" in data:
        tovar.opis = (data.get("opis") or "").strip() or tovar.opis
    if "tsina" in data:
        try:
            tovar.tsina = float(data.get("tsina"))
        except Exception:
            return jsonify(error="tsina must be a number"), 400

    db.session.commit()
    return jsonify(tovar.to_dict())


@api.delete("/tovars/<int:id>")
def delete_tovar(id):
    """
    ✅ Не падає, якщо є замовлення:
    - з ondelete="CASCADE" + PRAGMA foreign_keys=ON воно видалиться каскадом
    - додатково робимо rollback на випадок помилки
    """
    tovar = Tovar.query.get_or_404(id)

    try:
        db.session.delete(tovar)
        db.session.commit()
        return jsonify({"deleted": True})
    except Exception as e:
        db.session.rollback()
        return jsonify(error="Cannot delete tovar", detail=str(e)), 400


# ================== ORDERS ==================

@api.get("/orders")
def get_orders():
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return jsonify([o.to_dict() for o in orders])


@api.post("/orders")
def create_order():
    data = request.get_json(silent=True) or {}

    tovar_id = data.get("tovar_id")
    name = (data.get("name") or "").strip()
    phone = (data.get("phone") or "").strip()
    quantity = data.get("quantity", 1)

    if not tovar_id or not name or not phone:
        return jsonify(error="tovar_id/name/phone required"), 400

    try:
        quantity = int(quantity)
        if quantity < 1 or quantity > 99:
            return jsonify(error="quantity must be 1..99"), 400
    except Exception:
        return jsonify(error="quantity must be integer"), 400

    # Перевіримо, що товар існує (щоб не було FK error)
    tovar = Tovar.query.get(tovar_id)
    if not tovar:
        return jsonify(error="tovar not found"), 404

    order = Order(
        tovar_id=tovar_id,
        name=name,
        phone=phone,
        quantity=quantity,
        status="NEW"  # ✅ Нове поле
    )
    db.session.add(order)
    db.session.commit()
    return jsonify(order.to_dict()), 201


# ================== FEEDBACK ==================

@api.get("/feedbacks")
def get_feedbacks():
    feedbacks = Feedback.query.order_by(Feedback.created_at.desc()).all()
    return jsonify([f.to_dict() for f in feedbacks])


@api.post("/feedbacks")
def create_feedback():
    data = request.get_json(silent=True) or {}

    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip()
    message = (data.get("message") or "").strip()

    if not name or not email or not message:
        return jsonify(error="name/email/message required"), 400

    feedback = Feedback(name=name, email=email, message=message)
    db.session.add(feedback)
    db.session.commit()
    return jsonify(feedback.to_dict()), 201