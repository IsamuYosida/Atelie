from flask import Flask
from flask_login import LoginManager
from config import Config
from extensions import db, migrate
from models import User, Product, Material, Cart, Order
from routes import routes_bp

app = Flask(__name__)
app.config.from_object(Config)

# Инициализация Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# Инициализация базы данных и миграций
db.init_app(app)
migrate.init_app(app, db)
# Регистрация Blueprint
app.register_blueprint(routes_bp)

# Загрузка пользователя для Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Создание базы данных и добавление тестовых данных
with app.app_context():
    db.create_all()

    # Добавляем тестовые данные
    if not Product.query.first():
        # Тестовые модели
        products = [
            Product(name="Футболка", base_price=1000, image="images/t-shirt.jpg"),
            Product(name="Джинсы", base_price=2500, image="images/jeans.jpg"),
            Product(name="Платье", base_price=3000, image="images/dress.jpg"),
        ]
        db.session.add_all(products)

        # Тестовые материалы
        materials = [
            Material(name="Хлопок", price_per_meter=500),
            Material(name="Джинсовая ткань", price_per_meter=800),
            Material(name="Шёлк", price_per_meter=1200),
        ]
        db.session.add_all(materials)

        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)