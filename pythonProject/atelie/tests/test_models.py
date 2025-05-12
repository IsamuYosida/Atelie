import pytest
from models import User, Product, Order
from extensions import db


def test_user_model(app):
    """Test User model creation."""
    with app.app_context():
        # Очищаем перед тестом
        User.query.delete()

        user = User(username='testuser', password='testpass', is_employee=False)
        db.session.add(user)
        db.session.commit()

        assert user.username == 'testuser'
        assert user.password == 'testpass'
        assert not user.is_employee


def test_product_model(app):
    """Test Product model creation."""
    with app.app_context():
        # Очищаем перед тестом
        Product.query.delete()

        product = Product(name='Test Product', base_price=1000, image='test.jpg')
        db.session.add(product)
        db.session.commit()

        assert product.name == 'Test Product'
        assert product.base_price == 1000
        assert product.image == 'test.jpg'


def test_order_model(app):
    """Test Order model creation and methods."""
    with app.app_context():
        # Очищаем перед тестом
        User.query.delete()
        Product.query.delete()
        Order.query.delete()

        user = User(username='testuser', password='testpass')
        product = Product(name='Test Product', base_price=1000)
        db.session.add_all([user, product])
        db.session.commit()

        order = Order(
            user_id=user.id,
            product_id=product.id,
            size='M',
            color='red',
            quantity=1,
            total_price=1000,
            status='Ожидает подтверждения'
        )
        db.session.add(order)
        db.session.commit()

        assert order.is_custom() is False
        assert order.status == 'Ожидает подтверждения'
        assert order.total_price == 1000