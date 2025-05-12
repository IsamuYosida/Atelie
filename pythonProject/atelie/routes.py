from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from .models import User, Product, Material, Cart, Order
from .extensions import db

routes_bp = Blueprint('routes', __name__)

@routes_bp.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

@routes_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        is_employee = 'is_employee' in request.form

        # Проверяем, существует ли пользователь с таким именем
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Пользователь с таким именем уже существует!', 'error')
            return redirect(url_for('routes.register'))

        new_user = User(username=username, password=password, is_employee=is_employee)
        db.session.add(new_user)
        db.session.commit()

        flash('Регистрация успешна!', 'success')
        return redirect(url_for('routes.login'))

    return render_template('register.html')

@routes_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            flash('Вход выполнен успешно!', 'success')
            return redirect(url_for('routes.index'))
        else:
            flash('Неверный логин или пароль', 'error')

    return render_template('login.html')

@routes_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы.', 'success')
    return redirect(url_for('routes.index'))

@routes_bp.route('/profile')
@login_required
def profile():
    user = current_user
    orders = Order.query.filter_by(user_id=user.id).all()
    return render_template('profile.html', user=user, orders=orders)

@routes_bp.route('/custom_order', methods=['GET', 'POST'])
@login_required
def custom_order():
    if request.method == 'POST':
        material_id = request.form['material']
        size = request.form['size']
        color = request.form['color']
        style = request.form['style']
        gender = request.form['gender']
        quantity = int(request.form['quantity'])

        # Логика для расчета стоимости и создания заказа
        material = Material.query.get(material_id)
        if not material:
            flash('Материал не найден', 'error')
            return redirect(url_for('routes.custom_order'))

        # Пример расчета стоимости
        total_price = material.price_per_meter * 2  # Примерная стоимость

        # Создаем запись в корзине для авторского заказа
        cart_item = Cart(
            user_id=current_user.id,
            size=size,
            color=color,
            quantity=quantity,
            custom_description=f"Авторский заказ: {style}, {gender}, материал: {material.name}",
            total_price=total_price
        )
        db.session.add(cart_item)
        db.session.commit()

        flash('Авторский заказ добавлен в корзину!', 'success')
        return redirect(url_for('routes.cart'))

    materials = Material.query.all()
    return render_template('custom_order.html', materials=materials)

@routes_bp.route('/employee_dashboard')
@login_required
def employee_dashboard():
    if not current_user.is_employee:
        flash('Доступ запрещен', 'error')
        return redirect(url_for('routes.index'))

    orders = Order.query.all()
    completed_orders = Order.query.filter_by(status="Завершен").all()

    # Расчет статистики
    total_revenue = sum(order.total_price for order in completed_orders)
    total_orders_completed = len(completed_orders)

    # Расчет ткани для авторских заказов
    fabric_used = {}
    for order in completed_orders:
        if order.custom_description:
            # Пример: 2 метра ткани на авторский заказ
            fabric_used[order.id] = 2
        elif order.product:
            # Пример: 1 метр ткани на обычный заказ
            fabric_used[order.id] = 1

    total_fabric_used = sum(fabric_used.values())

    return render_template(
        'employee_dashboard.html',
        orders=orders,
        total_revenue=total_revenue,
        total_orders_completed=total_orders_completed,
        total_fabric_used=total_fabric_used,
        fabric_used=fabric_used
    )

@routes_bp.route('/update_order_status/<int:order_id>', methods=['POST'])
@login_required
def update_order_status(order_id):
    if not current_user.is_employee:
        flash('Доступ запрещен', 'error')
        return redirect(url_for('routes.index'))

    order = Order.query.get(order_id)
    if not order:
        flash('Заказ не найден', 'error')
        return redirect(url_for('routes.employee_dashboard'))

    order.status = request.form['status']
    db.session.commit()

    flash('Статус заказа обновлен!', 'success')
    return redirect(url_for('routes.employee_dashboard'))

@routes_bp.route('/cart')
@login_required
def cart():
    user = current_user
    cart_items = Cart.query.filter_by(user_id=user.id).all()
    total_price = sum(item.product.base_price * item.quantity if item.product else item.total_price for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total_price=total_price)

@routes_bp.route('/add_to_cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    size = request.form['size']
    color = request.form['color']
    quantity = int(request.form['quantity'])

    cart_item = Cart.query.filter_by(user_id=current_user.id, product_id=product_id, size=size, color=color).first()
    if cart_item:
        cart_item.quantity += quantity
    else:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'success': False, 'message': 'Товар не найден!'})

        cart_item = Cart(
            user_id=current_user.id,
            product_id=product_id,
            size=size,
            color=color,
            quantity=quantity,
            total_price=product.base_price * quantity
        )
        db.session.add(cart_item)

    db.session.commit()
    return jsonify({'success': True, 'message': 'Товар добавлен в корзину!'})

@routes_bp.route('/remove_from_cart/<int:cart_id>')
@login_required
def remove_from_cart(cart_id):
    cart_item = Cart.query.get(cart_id)
    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()
        flash('Товар удален из корзины!', 'success')

    return redirect(url_for('routes.cart'))

@routes_bp.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    user = current_user
    cart_items = Cart.query.filter_by(user_id=user.id).all()

    if not cart_items:
        flash('Ваша корзина пуста!', 'error')
        return redirect(url_for('routes.cart'))

    if request.method == 'POST':
        for item in cart_items:
            if item.product:
                # Обычный товар
                order = Order(
                    user_id=user.id,
                    product_id=item.product_id,
                    size=item.size,
                    color=item.color,
                    quantity=item.quantity,
                    total_price=item.product.base_price * item.quantity,
                    status="Ожидает подтверждения"
                )
            else:
                # Авторский заказ
                order = Order(
                    user_id=user.id,
                    custom_description=item.custom_description,
                    size=item.size,
                    color=item.color,
                    quantity=item.quantity,
                    total_price=item.total_price,
                    status="Ожидает подтверждения"
                )
            db.session.add(order)

        # Очищаем корзину после оформления заказа
        Cart.query.filter_by(user_id=user.id).delete()
        db.session.commit()

        flash('Заказ успешно оформлен!', 'success')
        return redirect(url_for('routes.profile'))

    return render_template('checkout.html', cart_items=cart_items)