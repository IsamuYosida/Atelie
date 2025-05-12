import pytest
import os
from flask import url_for
from models import User, Product
from extensions import db


def test_index_route(client, app):
    """Test index route."""
    with app.app_context():
        # Создаем тестовый продукт с корректным путем к изображению
        test_image_path = "static/images/test_product.jpg"

        # Создаем пустой файл изображения, если его нет
        if not os.path.exists(test_image_path):
            os.makedirs(os.path.dirname(test_image_path), exist_ok=True)
            open(test_image_path, 'wb').close()

        # Удаляем старые продукты и добавляем новый
        Product.query.delete()
        product = Product(name="Test Product", base_price=1000, image=test_image_path)
        db.session.add(product)
        db.session.commit()

    # Тестируем главную страницу
    response = client.get('/')
    assert response.status_code == 200


def test_register_route(client, app):
    """Test user registration."""
    with app.app_context():
        User.query.delete()
        db.session.commit()

    # GET-запрос
    response = client.get('/register')
    assert response.status_code == 200

    # POST-запрос - регистрируем обычного пользователя (без is_employee)
    response = client.post('/register', data={
        'username': 'newuser',
        'password': 'newpass',
        # Поле is_employee не включаем для обычного пользователя
    }, follow_redirects=True)

    assert response.status_code == 200

    # Проверяем созданного пользователя
    with app.app_context():
        user = User.query.filter_by(username='newuser').first()
        assert user is not None
        assert user.is_employee == False  # Теперь должно проходить

    # POST-запрос - регистрируем сотрудника (с явным указанием is_employee)
    response = client.post('/register', data={
        'username': 'employee',
        'password': 'emppass',
        'is_employee': 'on'  # Явно указываем для сотрудника
    }, follow_redirects=True)

    assert response.status_code == 200

    with app.app_context():
        employee = User.query.filter_by(username='employee').first()
        assert employee is not None
        assert employee.is_employee == True

def test_login_logout_route(client, app):
    """Test login and logout functionality."""
    with app.app_context():
        User.query.delete()
        # Создаем тестового пользователя
        user = User(username='testuser', password='testpass', is_employee=False)
        db.session.add(user)
        db.session.commit()

    # Неправильные учетные данные
    response = client.post('/login', data={
        'username': 'testuser',
        'password': 'wrongpass'
    }, follow_redirects=True)
    assert response.status_code == 200

    # Правильные учетные данные
    response = client.post('/login', data={
        'username': 'testuser',
        'password': 'testpass'
    }, follow_redirects=True)
    assert response.status_code == 200

    # Выход из системы
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200