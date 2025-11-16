from flask import Blueprint, render_template, redirect, url_for, flash, request
from .models import Tovar, Feedback, Order
from .forms import FeedbackForm, OrderForm
from . import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/menu')
def menu():
    tovary = Tovar.query.all()
    return render_template('menu.html', tovary=tovary)

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
            quantity=form.quantity.data
        )
        db.session.add(new_order)
        db.session.commit()
        flash(f'Ваше замовлення на {tovar.nazva} прийнято!', 'success')
        return redirect(url_for('main.menu'))
    return render_template('order.html', form=form, tovar=tovar)
