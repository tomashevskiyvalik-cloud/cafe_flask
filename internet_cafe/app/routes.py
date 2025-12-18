from flask import Blueprint, render_template, redirect, url_for, flash, request
from sqlalchemy import or_

from .models import Tovar, Feedback, Order
from .forms import FeedbackForm, OrderForm
from . import db

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    return render_template('index.html')


@main_bp.route('/menu')
def menu():
    q = request.args.get('q', '').strip()
    sort = request.args.get('sort', 'new')  # new / price_asc / price_desc / name
    page = request.args.get('page', 1, type=int)

    query = Tovar.query

    if q:
        query = query.filter(or_(
            Tovar.nazva.ilike(f"%{q}%"),
            Tovar.opis.ilike(f"%{q}%")
        ))

    if sort == "price_asc":
        query = query.order_by(Tovar.tsina.asc())
    elif sort == "price_desc":
        query = query.order_by(Tovar.tsina.desc())
    elif sort == "name":
        query = query.order_by(Tovar.nazva.asc())
    else:
        query = query.order_by(Tovar.id.desc())

    pagination = query.paginate(page=page, per_page=6, error_out=False)

    return render_template(
        'menu.html',
        tovary=pagination.items,
        pagination=pagination,
        q=q,
        sort=sort
    )


@main_bp.route('/feedback', methods=['GET', 'POST'])
def feedback():
    form = FeedbackForm()
    if form.validate_on_submit():
        fb = Feedback(name=form.name.data, email=form.email.data, message=form.message.data)
        db.session.add(fb)
        db.session.commit()
        flash('Дякуємо за ваш відгук!', 'success')
        return redirect(url_for('main.feedback'))

    feedbacks = Feedback.query.order_by(Feedback.created_at.desc()).all()
    return render_template('feedback.html', form=form, feedbacks=feedbacks)


@main_bp.route('/order/<int:tovar_id>', methods=['GET', 'POST'])
def order(tovar_id):
    tovar = Tovar.query.get_or_404(tovar_id)
    form = OrderForm()

    if form.validate_on_submit():
        new_order = Order(
            tovar_id=tovar.id,
            name=form.name.data,
            phone=form.phone.data,
            quantity=form.quantity.data,
            status="NEW"
        )
        db.session.add(new_order)
        db.session.commit()
        flash(f'Ваше замовлення на {tovar.nazva} прийнято!', 'success')
        return redirect(url_for('main.menu'))

    return render_template('order.html', form=form, tovar=tovar)


@main_bp.route('/api-page')
def api_page():
    return render_template('api_page.html')