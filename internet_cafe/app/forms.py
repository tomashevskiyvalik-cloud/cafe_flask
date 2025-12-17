from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, FloatField, TextAreaField, SubmitField, EmailField, IntegerField
from wtforms.validators import DataRequired, Email, NumberRange


class TovarForm(FlaskForm):
    nazva = StringField('Назва страви', validators=[DataRequired()])
    opis = TextAreaField('Опис', validators=[DataRequired()])
    tsina = FloatField('Ціна', validators=[DataRequired()])

    # ✅ НОВЕ ПОЛЕ ДЛЯ ФОТО
    photo = FileField('Фото', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'webp'], 'Тільки зображення (jpg, jpeg, png, webp)!')
    ])

    submit = SubmitField('Зберегти')


class FeedbackForm(FlaskForm):
    name = StringField('Ім\'я', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    message = TextAreaField('Відгук', validators=[DataRequired()])
    submit = SubmitField('Надіслати')


class OrderForm(FlaskForm):
    name = StringField('Ім\'я', validators=[DataRequired()])
    phone = StringField('Телефон', validators=[DataRequired()])
    quantity = IntegerField('Кількість', validators=[DataRequired(), NumberRange(min=1)], default=1)
    submit = SubmitField('Замовити')
