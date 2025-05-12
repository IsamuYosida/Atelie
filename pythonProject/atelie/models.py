from datetime import datetime
from flask_login import UserMixin
from pythonProject.atelie.extensions import db


class User(db.Model, UserMixin):
    __tablename__ = 'users'  # Явное указание имени таблицы

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_employee = db.Column(db.Boolean, default=False)
    orders = db.relationship('Order', backref='user', lazy=True)
    carts = db.relationship('Cart', backref='user', lazy=True)


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    base_price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(200))
    orders = db.relationship('Order', backref='product', lazy=True)
    carts = db.relationship('Cart', backref='product', lazy=True)


class Material(db.Model):
    __tablename__ = 'materials'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price_per_meter = db.Column(db.Float, nullable=False)
    orders = db.relationship('Order', backref='material', lazy=True)


class Cart(db.Model):
    __tablename__ = 'carts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    size = db.Column(db.String(50), nullable=False)
    color = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    custom_description = db.Column(db.String(500))
    total_price = db.Column(db.Float, nullable=False)


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    material_id = db.Column(db.Integer, db.ForeignKey('materials.id'))
    custom_description = db.Column(db.String(500))
    size = db.Column(db.String(50), nullable=False)
    color = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), default="Ожидает подтверждения")
    total_price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def is_custom(self):
        return bool(self.custom_description)