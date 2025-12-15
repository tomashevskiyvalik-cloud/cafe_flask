# Звіт з лабораторної роботи 4

## Реалізація бази даних для вебпроєкту

### Інформація про команду
- Назва команди: **Смурфікі**

- Учасники:
  - **Томашевський Валентин Дмитрович** — лідер, проєктування структури БД, ORM моделі
  - **Михайло Чижук Михайлович** — backend логіка, маршрути, CRUD
  - **Максим Римарук Олександрович** — UI, стилізація інтерфейсу, адмін-панель

## Завдання

### Обрана предметна область

Система керування інтернет-кафе з підтримкою адміністрування меню, приймання замовлень, обліку відвідувань та управління асортиментом напоїв.

### Реалізовані вимоги

- [x] Рівень 1: базова БД, CRUD, відображення даних
- [x] Рівень 2: додаткові таблиці та логіка адміністрування
- [x] Рівень 3: UI розширення та покращення зручності використання

## Хід виконання роботи

### Підготовка середовища розробки

- Python 3.10
- Flask, flask_sqlalchemy, flask_migrate
- SQLite3
- Стилі: CSS, базові елементи UI Bootstrap

### Структура проєкту

Наведіть структуру файлів та директорій вашого проєкту:

```
CAFÉ_FLASK/
│
├── internet_cafe/
│   └── app/
│       ├── __pycache__/
│       ├── static/
│       │   ├── uploads/
│       │   ├── images/
│       │   └── style.css
│       │
│       ├── templates/
│       │   ├── add_tovar.html
│       │   ├── admin_feedback.html
│       │   ├── admin_tovar.html
│       │   ├── admin.html
│       │   ├── base.html
│       │   ├── edit_feedback.html
│       │   ├── edit_tovar.html
│       │   ├── feedback.html
│       │   ├── index.html
│       │   ├── menu.html
│       │   ├── order.html
│       │   └── zamovlennya.html
│       │
│       ├── __init__.py
│       ├── admin_routes.py
│       ├── app.py
│       ├── forms.py
│       ├── models.py
│       └── routes.py
│
├── instance/
│
├── routes/
│   ├── __init__.py
│   ├── admin.py
│   ├── feedback.py
│   └── shop.py
│
├── create_db.py
├── db.sqlite
├── fill_db.py
│
├── migrations/
│
├── venv/
│
├── .gitignore
├── config.py
├── requirements.txt
└── run.py

```

### Проектування бази даних

#### Схема бази даних

Опишіть структуру вашої бази даних:

```
Таблиця "feedback":
- id (INTEGER, PRIMARY KEY)
- name (TEXT, NOT NULL)
- email (TEXT, NOT NULL)
- message (TEXT, NOT NULL)
- created_at (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)

Таблиця "tovar":
- id (INTEGER, PRIMARY KEY)
- nazva (TEXT, NOT NULL)
- opis (TEXT, NOT NULL)
- tsina (REAL, NOT NULL)

Таблиця "order":
- id (INTEGER, PRIMARY KEY)
- tovar_id (INTEGER, FOREIGN KEY -> tovar.id, NOT NULL)
- name (TEXT, NOT NULL)
- phone (TEXT, NOT NULL)
- quantity (INTEGER, DEFAULT 1)
- created_at (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)

```



### Опис реалізованої функціональності

#### Система відгуків

Користувачі можуть залишати відгуки через форму з іменем, email та текстом повідомлення. Відгуки зберігаються у базі та відображаються на сторінці відгуків. Адмін може переглядати та видаляти відгуки.

#### Магазин

Опишіть функціональність магазину:

* Відображення каталогу страв (товарів) з назвою, описом та ціною.
* Біля кожної страви є кнопка "Замовити", яка веде до форми замовлення.
* У формі замовлення користувач вводить ім'я, телефон, кількість.
* Після відправлення замовлення дані зберігаються у базі.

#### Адміністративна панель

Опишіть можливості адмін-панелі:

Адмін-панель дозволяє:

* Переглядати всі товари (страви), додавати, редагувати, видаляти.
* Переглядати відгуки користувачів та видаляти їх.
* Переглядати замовлення клієнтів з інформацією про страву, замовника, кількість і дату, а також видаляти замовлення.
#### Додаткова функціональність (якщо реалізовано)

Додатково було реалізовано валідацію форм за допомогою Flask-WTF, що покращує якість введених користувачем даних.

## Ключові фрагменти коду

### Ініціалізація бази даних

Наведіть код створення таблиць у файлі `models.py`:

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

### CRUD операції

Наведіть приклади реалізації CRUD операцій:

#### Створення (Create)

def add_feedback(name, email, message):
    new_fb = Feedback(name=name, email=email, message=message)
    db.session.add(new_fb)
    db.session.commit()

```

#### Читання (Read)

```Python
def get_all_feedback():
    return Feedback.query.order_by(Feedback.created_at.desc()).all()

```

#### Оновлення (Update)

```python
def update_order_status(order_id, status):
    order = Order.query.get(order_id)
    if order:
        order.status = status
        db.session.commit()

```

#### Видалення (Delete)

```python
def delete_feedback(feedback_id):
    fb = Feedback.query.get(feedback_id)
    if fb:
        db.session.delete(fb)
        db.session.commit()

```

### Маршрутизація

Наведіть приклади маршрутів для роботи з базою даних:

```python
@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    form = FeedbackForm()
    if form.validate_on_submit():
        add_feedback(form.name.data, form.email.data, form.message.data)
        flash('Дякуємо за ваш відгук!', 'success')
        return redirect(url_for('feedback'))
    feedbacks = get_all_feedback()
    return render_template('feedback.html', form=form, feedbacks=feedbacks)

```

### Робота зі зв'язками між таблицями

Наведіть приклад запиту з використанням JOIN для отримання пов'язаних даних:

```python
def get_order_details(order_id):
    return db.session.query(Order, Tovar).join(Tovar).filter(Order.id == order_id).first()


#### Роль у команді — **Римарук М.О.**

- верстка інтерфейсу меню
- побудова HTML шаблонів Jinja2
- стилізація елементів форм
- підтримка UX при заповненні замовлень
- дизайн адмін-розділу

## Скріншоти

Додайте скріншоти основних функцій вашого вебзастосунку:

### Головна сторінка

![Головна сторінка](https://media.discordapp.net/attachments/1291374970907136061/1439676724282654872/image.png?ex=691b62ee&is=691a116e&hm=f8485c3a6b09efda279d6c15fb924effd0dd54cf3d79dbd70fbd9db323526599&=&format=webp&quality=lossless&width=1803&height=864)

### Каталог товарів

![Каталог товарів](https://media.discordapp.net/attachments/1291374970907136061/1439676998191550494/image.png?ex=691b6330&is=691a11b0&hm=bcd7a2af697deb593a9ec0180b6784642c2a03b21771a7dea257a4973b9d356e&=&format=webp&quality=lossless&width=1789&height=864)

### Адміністративна панель

![Адмін-панель] (https://media.discordapp.net/attachments/1291374970907136061/1439677110183526501/image.png?ex=691b634a&is=691a11ca&hm=717f919b156cfe96ff3972ba4a32b768a5b8b83fecd143e1c4bf36de089f88c6&=&format=webp&quality=lossless&width=1789&height=864)

### Управління замовленнями

![Управління замовленнями](https://media.discordapp.net/attachments/1291374970907136061/1439677292405067929/image.png?ex=691b6376&is=691a11f6&hm=178a0c6bb86b7a72ffe1d1ecd14f4d7218cb7679f2af47b3817bcec745a338fb&=&format=webp&quality=lossless&width=1781&height=864)

### Додаткова функціональність

![Додаткова функція](шлях/до/скріншоту)

## Тестування

- перевірка верстки на адаптивність
- коректність візуалізації замовлень
- тестування шаблонів та контекстних змінних

## Висновки

Розроблено адаптивний та інтуїтивний інтерфейс для користувачів і адміністрації. Закріплено навички інтеграції фронтенду з backend API, структурування шаблонів та покращення користувацького досвіду.

**Очікувана оцінка:** 7/12 балів

