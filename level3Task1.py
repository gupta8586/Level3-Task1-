from Flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Paths to store data
PRODUCT_FILE = 'products.json'
USER_FILE = 'users.json'
ORDER_FILE = 'orders.json'

# Load data from file
def load_data(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return json.load(f)
    return {}

# Save data to file
def save_data(file_path, data):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

# Route for home page
@app.route('/')
def index():
    products = load_data(PRODUCT_FILE)
    return render_template('index.html', products=products)

# Route for viewing a product
@app.route('/product/<product_id>')
def product(product_id):
    products = load_data(PRODUCT_FILE)
    product = products.get(product_id)
    return render_template('product.html', product=product)

# Route for adding to cart
@app.route('/add_to_cart/<product_id>', methods=['POST'])
def add_to_cart(product_id):
    products = load_data(PRODUCT_FILE)
    product = products.get(product_id)
    if 'cart' not in session:
        session['cart'] = {}
    cart = session['cart']
    if product_id in cart:
        cart[product_id]['quantity'] += 1
    else:
        cart[product_id] = {'name': product['name'], 'price': product['price'], 'quantity': 1}
    session['cart'] = cart
    return redirect(url_for('index'))

# Route for viewing cart
@app.route('/cart')
def cart():
    return render_template('cart.html')

# Route for checkout
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        # Save the order
        orders = load_data(ORDER_FILE)
        order_id = str(len(orders) + 1)
        orders[order_id] = session['cart']
        save_data(ORDER_FILE, orders)
        session.pop('cart', None)
        return render_template('checkout.html', success=True)
    return render_template('checkout.html')

# User login (simplified)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        users = load_data(USER_FILE)
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('index'))
    return render_template('login.html')

# User logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
