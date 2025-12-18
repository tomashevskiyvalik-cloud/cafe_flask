from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, FloatField, TextAreaField, SubmitField, EmailField, IntegerField
from wtforms.validators import DataRequired, Email, NumberRange, Length, Regexp


class TovarForm(FlaskForm):
    nazva = StringField('Назва страви', validators=[DataRequired()])
    opis = TextAreaField('Опис', validators=[DataRequired()])
    tsina = FloatField('Ціна', validators=[DataRequired()])

    photo = FileField('Фото', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'webp'], 'Тільки зображення (jpg, jpeg, png, webp)!')
    ])

    submit = SubmitField('Зберегти')


class FeedbackForm(FlaskForm):
    name = StringField("Ім'я", validators=[DataRequired(), Length(min=2, max=100)])
    email = EmailField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    message = TextAreaField('Відгук', validators=[DataRequired(), Length(min=5, max=2000)])
    submit = SubmitField('Надіслати')


class OrderForm(FlaskForm):
    name = StringField("Ім'я", validators=[DataRequired(), Length(min=2, max=100)])

    phone = StringField('Телефон', validators=[
        DataRequired(),
        Length(min=8, max=20),
        Regexp(r'^[0-9+\-\s()]+$', message="Невірний формат телефону")
    ])

    quantity = IntegerField('Кількість', validators=[DataRequired(), NumberRange(min=1, max=99)], default=1)
    submit = SubmitField('Замовити')