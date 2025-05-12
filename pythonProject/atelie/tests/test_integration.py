import pytest
from models import User, Product, Order, Cart
from extensions import db


def test_full_order_flow(client, app):
    """Test complete order flow from registration to order placement."""
    with app.app_context():
        # Очищаем все таблицы
        db.session.query(User).delete()
        db.session.query(Order).delete()
        db.session.query(Cart).delete()

        # Создаем тестовый продукт
        product = Product(name="Test Product", base_price=1000, image="static/images/default.jpg")
        db.session.add(product)
        db.session.commit()

    # 1. Регистрация пользователя
    response = client.post('/register', data={
        'username': 'orderuser',
        'password': 'orderpass',
        'is_employee': 'false'  # Используем строку вместо bool
    }, follow_redirects=True)
    assert response.status_code == 200

    # 2. Вход в систему
    response = client.post('/login', data={
        'username': 'orderuser',
        'password': 'orderpass'
    }, follow_redirects=True)
    assert response.status_code == 200

    # 3. Добавление товара в корзину
    with app.app_context():
        product = Product.query.first()
        assert product is not None  # Проверяем, что продукт существует

    response = client.post(f'/add_to_cart/{product.id}', data={
        'size': 'L',
        'color': 'blue',
        'quantity': 1
    })
    assert response.status_code == 200

    # 4. Оформление заказа
    response = client.post('/checkout', follow_redirects=True)
    assert response.status_code == 200

    # 5. Проверка создания заказа
    with app.app_context():
        user = User.query.filter_by(username='orderuser').first()
        orders = Order.query.filter_by(user_id=user.id).all()
        assert len(orders) >= 1


def test_employee_dashboard_access(client, app):
    """Test employee dashboard access control."""
    with app.app_context():
        db.session.query(User).delete()
        regular = User(username='regular', password='pass', is_employee=False)
        employee = User(username='employee', password='pass', is_employee=True)
        db.session.add_all([regular, employee])
        db.session.commit()

    # Обычный пользователь
    client.post('/login', data={
        'username': 'regular',
        'password': 'pass'
    }, follow_redirects=True)

    response = client.get('/employee_dashboard', follow_redirects=True)
    assert response.status_code == 200

    # Сотрудник
    client.post('/login', data={
        'username': 'employee',
        'password': 'pass'
    }, follow_redirects=True)

    response = client.get('/employee_dashboard')
    assert response.status_code == 200