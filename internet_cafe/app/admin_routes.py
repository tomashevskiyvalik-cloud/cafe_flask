import os
from uuid import uuid4

from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from werkzeug.utils import secure_filename

from .models import Tovar, Feedback, Order
from .forms import TovarForm
from . import db

admin_bp = Blueprint('admin', __name__)

ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp'}


def _uploads_dir():
    # internet_cafe/app/static/uploads/tovary
    return os.path.join(current_app.root_path, 'static', 'uploads', 'tovary')


def _save_photo(file_storage):
    """
    Save uploaded image into static/uploads/tovary and return filename.
    Returns None if no file provided.
    """
    if not file_storage or not getattr(file_storage, "filename", ""):
        return None

    ext = os.path.splitext(file_storage.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        return None

    os.makedirs(_uploads_dir(), exist_ok=True)

    filename = secure_filename(f"{uuid4().hex}{ext}")
    file_storage.save(os.path.join(_uploads_dir(), filename))
    return filename


def _delete_photo(filename):
    if not filename:
        return
    path = os.path.join(_uploads_dir(), filename)
    try:
        if os.path.exists(path):
            os.remove(path)
    except Exception:
        # не ламаємо сайт, навіть якщо файл не видалився
        pass


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
        filename = _save_photo(form.photo.data)

        new_tovar = Tovar(
            nazva=form.nazva.data,
            opis=form.opis.data,
            tsina=form.tsina.data,
            image_filename=filename
        )
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

        # якщо завантажили нове фото — заміняємо старе
        if form.photo.data and getattr(form.photo.data, "filename", ""):
            new_filename = _save_photo(form.photo.data)
            if new_filename:
                _delete_photo(tovar.image_filename)
                tovar.image_filename = new_filename

        db.session.commit()
        flash('Страву оновлено!', 'success')
        return redirect(url_for('admin.admin_index'))

    return render_template('edit_tovar.html', form=form, tovar=tovar)


@admin_bp.route('/delete_tovar/<int:id>', methods=['POST'])
def delete_tovar(id):
    tovar = Tovar.query.get_or_404(id)

    # видаляємо фото з диска
    _delete_photo(tovar.image_filename)

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