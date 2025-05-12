import pytest
import os
import tempfile
import sys
from pathlib import Path

# Фикс для дублирования моделей
from sqlalchemy import MetaData

metadata = MetaData()

# Добавляем путь к проекту
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pythonProject.atelie.extensions import db

db.metadata = metadata  # Используем единый MetaData


@pytest.fixture(scope='session')
def app():
    """Глобальная фикстура приложения"""
    from pythonProject.atelie.app import app as flask_app

    # Настройка тестовой БД
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    flask_app.config['TESTING'] = True
    flask_app.config['WTF_CSRF_ENABLED'] = False

    with flask_app.app_context():
        db.create_all()
        yield flask_app
        db.drop_all()


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