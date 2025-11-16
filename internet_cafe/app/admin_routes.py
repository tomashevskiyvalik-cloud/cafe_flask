from flask import Blueprint, render_template, redirect, url_for, flash, request
from .models import Tovar, Feedback, Order
from .forms import TovarForm
from . import db

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/')
def admin_index():
    tovary = Tovar.query.all()
    feedbacks = Feedback.query.order_by(Feedback.created_at.desc()).all()
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template('admin.html', tovary=tovary, feedbacks=feedbacks, orders=orders)

@admin_bp.route('/add_tovar', methods=['GET', 'POST'])
def add_tovar():
    form = TovarForm()
    if form.validate_on_submit():
        new_tovar = Tovar(nazva=form.nazva.data, opis=form.opis.data, tsina=form.tsina.data)
        db.session.add(new_tovar)
        db.session.commit()
        flash('Страву додано!', 'success')
        return redirect(url_for('admin.admin_index'))
    return render_template('add_tovar.html', form=form)

@admin_bp.route('/edit_tovar/<int:id>', methods=['GET', 'POST'])
def edit_tovar(id):
    tovar = Tovar.query.get_or_404(id)
    form = TovarForm(obj=tovar)
    if form.validate_on_submit():
        tovar.nazva = form.nazva.data
        tovar.opis = form.opis.data
        tovar.tsina = form.tsina.data
        db.session.commit()
        flash('Страву оновлено!', 'success')
        return redirect(url_for('admin.admin_index'))
    return render_template('edit_tovar.html', form=form)

@admin_bp.route('/delete_tovar/<int:id>', methods=['POST'])
def delete_tovar(id):
    tovar = Tovar.query.get_or_404(id)
    db.session.delete(tovar)
    db.session.commit()
    flash('Страву видалено!', 'info')
    return redirect(url_for('admin.admin_index'))

@admin_bp.route('/delete_feedback/<int:id>', methods=['POST'])
def delete_feedback(id):
    fb = Feedback.query.get_or_404(id)
    db.session.delete(fb)
    db.session.commit()
    flash('Відгук видалено!', 'info')
    return redirect(url_for('admin.admin_index'))

@admin_bp.route('/delete_order/<int:id>', methods=['POST'])
def delete_order(id):
    order = Order.query.get_or_404(id)
    db.session.delete(order)
    db.session.commit()
    flash('Замовлення видалено!', 'info')
    return redirect(url_for('admin.admin_index'))
