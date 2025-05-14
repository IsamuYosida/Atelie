import pytest
from app import app as flask_app
from extensions import db
from models import User, Product, Material, Cart, Order
import os
import tempfile


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # Создаем временную базу данных
    db_fd, db_path = tempfile.mkstemp()
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
    flask_app.config['TESTING'] = True
    flask_app.config['WTF_CSRF_ENABLED'] = False

    with flask_app.app_context():
        db.create_all()
        # Добавляем тестовые данные
        products = [
            Product(name="Футболка", base_price=1000, image="images/t-shirt.jpg"),
            Product(name="Джинсы", base_price=2500, image="images/jeans.jpg"),
        ]
        db.session.add_all(products)

        materials = [
            Material(name="Хлопок", price_per_meter=500),
            Material(name="Джинсовая ткань", price_per_meter=800),
        ]
        db.session.add_all(materials)
        db.session.commit()

    yield flask_app

    # Удаляем временную базу после тестов
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()


@pytest.fixture(autouse=True)
def cleanup_test_data(app):
    """Фикстура для автоматической очистки тестовых данных после каждого теста"""
    yield
    with app.app_context():
        # Удаляем все заказы перед удалением продуктов
        Order.query.delete()  # Сначала удаляем заказы
        Product.query.filter(Product.name.in_(["Test Product", "Футболка", "Джинсы"])).delete()
        db.session.commit()
