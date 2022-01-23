from itertools import product
from flask import render_template, request, session, redirect, g
import flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import selectin_polymorphic
from qbay.models import login, User, register, updateUserLogin, Product, \
    createProduct, updateProduct, Review, updateBalance, productOrder
from datetime import timezone
import datetime
from qbay import app


def authenticate(inner_function):
    """
    :param inner_function: any python function that accepts a user object
    Wrap any python function and check the current session to see if
    the user has logged in. If login, it will call the inner_function
    with the logged in user object.
    To wrap a function, we can put a decoration on that function.
    Example:
    @authenticate
    def home_page(user):
        pass
    """

    def wrapped_inner():

        # check did we store the key in the session
        if 'logged_in' in session:
            email = session['logged_in']
            try:
                user = User.query.filter_by(email=email).first()
                if user:
                    # if the user exists, call the inner_function
                    # with user as parameter
                    return inner_function(user)
            except Exception:
                pass
        else:
            # else, redirect to the login page
            return redirect('/login')

    # return the wrapped version of the inner_function:
    # Renaming the function name:
    wrapped_inner.__name__ = inner_function.__name__
    return wrapped_inner


@app.route('/login', methods=['GET'])
def login_get():
    return render_template('login.html', message='Please login')


@app.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    user = login(email, password)
    if user:
        session['logged_in'] = user.email
        """
        Session is an object that contains sharing information
        between a user's browser and the end server.
        Typically it is packed and stored in the browser cookies.
        They will be past along between every request the browser made
        to this services. Here we store the user object into the
        session, so we can tell if the client has already login
        in the following sessions.
        """
        # success! go back to the home page
        # code 303 is to force a 'GET' request
        return redirect('/', code=303)
    else:
        return render_template('login.html', message='login failed')


@app.route('/')
@authenticate
def home(user):
    # authentication is done in the wrapper function
    # see above.
    # by using @authenticate, we don't need to re-write
    # the login checking code all the time for other
    # front-end portals
    if(session.get('message') is None):
        message = ' '
    else:
        message = session['message']
        flask.session.pop('message', None)
    products = Product.query.filter_by(owner_email = user.email).all()
    return render_template('index.html', user=user, products=products, message=message)


@app.route('/register', methods=['GET'])
def register_get():
    # templates are stored in the templates folder
    return render_template('register.html', message='')


@app.route('/register', methods=['POST'])
def register_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    error_message = None

    if password != password2:
        error_message = "The passwords do not match"
    else:
        # use backend api to register the user
        success = register(name, email, password)
        if not success:
            error_message = "Registration failed."
    # if there is any error messages when registering new user
    # at the backend, go back to the register page.
    if error_message:
        return render_template('register.html', message=error_message)
    else:
        return redirect('/login')


@app.route('/logout')
def logout():
    if 'logged_in' in session:
        session.pop('logged_in', None)
    return redirect('/')


@app.route('/profile_update', methods=['GET'])
@authenticate
def profile_update_get(user):
    # templates are stored in the templates folder
    return render_template('profile_update.html', user=user)


@app.route('/profile_update', methods=['POST'])
@authenticate
def profile_update_post(user):
    name = request.form.get('name')
    shippingAddress = request.form.get('address')
    postalCode = request.form.get('postal')
    newBalance = user.balance + int(request.form.get('addBalance'))
    error_message = None
    # use backend api to register the user
    success = updateUserLogin (user.email, user.password, name,
                              postalCode, shippingAddress)
    if success is None:
        error_message = "Failed to update profile"
    else:
        success = updateBalance(user, newBalance)
    
    if success is False:
        error_message = "Failed to update balance"
    # if there is any error messages when updating user
    # at the backend, reload the page.
    if error_message:
        return render_template('profile_update.html', message=error_message)
    else:
        return redirect('/')


@app.route('/create_product', methods=['GET'])
def create_product_get():
    # templates are stored in the templates folder
    return render_template('create_product.html', message='')


@app.route('/create_product', methods=['POST'])
def create_product_post():
    title = request.form.get('title')
    price = request.form.get('price')
    description = request.form.get('description')
    quantity = request.form.get('quantity')
    email = request.form.get('email')
    date = datetime.datetime.utcnow()
    error_message = None

    # use backend api to register the product
    success = createProduct(title, price, description, quantity, email, date)
    print(success)
    if not success:
        error_message = "Product creation failed."
    # if there is any error messages when registering new product
    # at the backend, go back to the creation page.
    if error_message:
        return render_template('create_product.html', message=error_message)
    else:
        return redirect('/')


@app.route('/product_update', methods=['GET'])
def product_update_get():
    # templates are stored in the templates folder
    return render_template('product_update.html', message='')


@app.route('/product_update', methods=['POST'])
def product_update_post():
    id = request.form.get('id')
    email = request.form.get('email')
    title = request.form.get('title')
    price = request.form.get('price')
    description = request.form.get('description')
    quantity = request.form.get('quantity')
    error_message = None
    # use backend api to update the product
    success = updateProduct(id, title, price, description, quantity)
    if success is None:
        error_message = "Failed to update product"
    # if there is any error messages when registering new user
    # at the backend, go back to the register page.
    if error_message:
        return render_template('product_update.html', message=error_message)
    else:
        return redirect('/login')

@app.route('/shop', methods=['GET'])
@authenticate
def shop_get(user):
    # templates are stored in the templates folder
    products = Product.query.filter(Product.quantity > 0, Product.owner_email != user.email)
    return render_template('shop.html', products=products)

@app.route('/shop', methods=['POST'])
def shop_post():
    # templates are stored in the templates folder
    productTitle = request.form.get('product_select')
    product = Product.query.filter_by(title=productTitle).first()
    session['product'] = product.title
    return redirect('/product_page')

@app.route('/product_page', methods=['GET'])
def product_page_get():
    # templates are stored in the templates folder
    productTitle = session['product']
    flask.session.pop('product', None)
    product = Product.query.filter_by(title=productTitle).first()
    title = product.title
    desc = product.description
    price = product.price
    return render_template('product_page.html', title=title, price=price, desc=desc)

@app.route('/product_page', methods=['POST'])
@authenticate
def product_page_post(user):
    # templates are stored in the templates folder
    product = request.form.get('title')
    product = Product.query.filter_by(title=product).first()
    productReturn = productOrder(product, user)
    if(productReturn is False):
        session['message'] = "There is not enough money in your balance or the item is unavailable."
        return redirect('/')
    else:
        session['message'] = "Product purchase is successful!"
        return redirect('/')

