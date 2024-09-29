from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user
from app import app, db
from models import User, Product, Customer, Sale


# Home Page
@app.route('/')
def home():
    return render_template('login.html')


# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:  # Use hashed passwords in production!
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check username and password.', 'danger')

    return render_template('login.html')


# Dashboard Route
@app.route('/dashboard')
@login_required  # Protect this route to only logged-in users.
def dashboard():
    return render_template('dashboard.html')


# Manage Products Route
@app.route('/manage_products', methods=['GET', 'POST'])
@login_required
def manage_products():
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        price = float(request.form['price'])
        quantity = int(request.form['quantity'])

        new_product = Product(name=name, category=category, price=price, quantity=quantity)
        db.session.add(new_product)
        db.session.commit()

        flash('Product added successfully!', 'success')

    products = Product.query.all()
    return render_template('manage_products.html', products=products)


# Manage Customers Route
@app.route('/manage_customers', methods=['GET', 'POST'])
@login_required
def manage_customers():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        new_customer = Customer(name=name, email=email, phone=phone)
        db.session.add(new_customer)
        db.session.commit()

        flash('Customer added successfully!', 'success')

    customers = Customer.query.all()
    return render_template('manage_customers.html', customers=customers)


# Record Sale Route
@app.route('/record_sale', methods=['GET', 'POST'])
@login_required
def record_sale():
    if request.method == 'POST':
        product_id = int(request.form['product_id'])
        customer_id = int(request.form['customer_id'])
        quantity = int(request.form['quantity'])

        product = Product.query.get(product_id)

        if product and product.quantity >= quantity:
            total_price = product.price * quantity

            new_sale = Sale(product_id=product_id, customer_id=customer_id, quantity=quantity, total_price=total_price)
            db.session.add(new_sale)

            # Update product quantity
            product.quantity -= quantity

            # Update customer loyalty points (1 point for every 10 units sold)
            customer = Customer.query.get(customer_id)
            customer.loyalty_points += quantity // 10

            db.session.commit()
            flash('Sale recorded successfully!', 'success')
        else:
            flash('Insufficient stock or invalid product.', 'danger')

    products = Product.query.all()
    customers = Customer.query.all()
    return render_template('record_sale.html', products=products, customers=customers)


# Logout Route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))