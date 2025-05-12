import pytest
import os
import tempfile
import sys
from pathlib import Path

# Важно: добавляем родительскую директорию в PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import app as flask_app
from extensions import db
from models import User, Product, Material, Cart, Order

# Флаг для CI
is_ci = os.environ.get('GITHUB_ACTIONS') == 'true'

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # Настройка БД
    if is_ci:
        flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    else:
        db_fd, db_path = tempfile.mkstemp()
        flask_app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

    flask_app.config['TESTING'] = True
    flask_app.config['WTF_CSRF_ENABLED'] = False

    with flask_app.app_context():
        db.create_all()
        if not is_ci:  # Добавляем тестовые данные только локально
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

    # Очистка (только для локальных тестов)
    if not is_ci:
        os.close(db_fd)
        os.unlink(db_path)

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

@pytest.fixture(autouse=True)
def cleanup_db(app):
    """Автоматическая очистка БД после тестов"""
    yield
    with app.app_context():
        db.session.query(Order).delete()
        db.session.query(Cart).delete()
        db.session.query(Product).delete()
        db.session.query(Material).delete()
        db.session.query(User).delete()
        db.session.commit()