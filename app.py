from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from models import db, User, Product, Customer, Sale
from forms import RegistrationForm  # Import the registration form

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///supermarket.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Suppress the warning

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def home():
    return render_template('login.html')


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


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        new_user = User(username=form.username.data,
                        email=form.email.data,
                        password=form.password.data)  # Hash this password in production!

        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route('/manage_products', methods=['GET', 'POST'])
@login_required
def manage_products():
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        price = float(request.form['price'])
        quantity = int(request.form['quantity'])

        new_product = Product(name=name, category=category, price=price,
                              quantity=quantity)

        db.session.add(new_product)
        db.session.commit()

        flash('Product added successfully!', 'success')

    # Handle search functionality
    search_query = request.args.get('search')

    if search_query:
        products = Product.query.filter(Product.name.ilike(f'%{search_query}%')).all()  # Case-insensitive search
    else:
        products = Product.query.all()  # Fetch all products if no search query

    return render_template('manage_products.html', products=products)


@app.route('/delete_product/<int:product_id>', methods=['POST'])
@login_required
def delete_product(product_id):
    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
        flash('Product deleted successfully!', 'success')
    else:
        flash('Product not found.', 'danger')

    return redirect(url_for('manage_products'))


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

    # Handle search functionality
    search_query = request.args.get('search')

    if search_query:
        customers = Customer.query.filter(Customer.name.ilike(f'%{search_query}%')).all()  # Case-insensitive search
    else:
        customers = Customer.query.all()  # Fetch all customers if no search query

    return render_template('manage_customers.html', customers=customers)


@app.route('/delete_customer/<int:customer_id>', methods=['POST'])
@login_required
def delete_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if customer:
        db.session.delete(customer)
        db.session.commit()
        flash('Customer deleted successfully!', 'success')
    else:
        flash('Customer not found.', 'danger')

    return redirect(url_for('manage_customers'))


@app.route('/record_sale', methods=['GET', 'POST'])
@login_required
def record_sale():
    if request.method == 'POST':
        product_id = int(request.form['product_id'])
        customer_id = int(request.form['customer_id'])  # Get selected customer ID
        quantity = int(request.form['quantity'])

        product = Product.query.get(product_id)

        if product and product.quantity >= quantity:
            total_price = product.price * quantity

            new_sale = Sale(product_id=product_id,
                            customer_id=customer_id,
                            quantity=quantity,
                            total_price=total_price)

            # Update product quantity
            product.quantity -= quantity

            db.session.add(new_sale)
            db.session.commit()
            flash('Sale recorded successfully!', 'success')

            # Notify if quantity goes below threshold after sale
            if product.quantity <= product.low_stock_threshold:
                flash(f'Warning: {product.name} is now low on stock!', 'warning')

        else:
            flash('Insufficient stock or invalid product.', 'danger')

    products = Product.query.all()
    customers = Customer.query.all()  # Fetch all customers for the dropdown

    return render_template('record_sale.html', products=products, customers=customers)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)