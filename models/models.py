import re
from datetime import timezone
import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from qbay import app


# Setting up regular expressions

RFC5322_REGEX = r'([!#-\'*+/-9=?A-Z^-~-]+(\.[!#-\'*+/-9=?A-Z^-~-]+)*|"([]!#-[^-~ \t]|(\\[\t -~]))+")@([0-9A-Za-z]([0-9A-Za-z-]{0,61}[0-9A-Za-z])?(\.[0-9A-Za-z]([0-9A-Za-z-]{0,61}[0-9A-Za-z])?)*|\[((25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])(\.(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])){3}|IPv6:((((0|[1-9A-Fa-f][0-9A-Fa-f]{0,3}):){6}|::((0|[1-9A-Fa-f][0-9A-Fa-f]{0,3}):){5}|[0-9A-Fa-f]{0,4}::((0|[1-9A-Fa-f][0-9A-Fa-f]{0,3}):){4}|(((0|[1-9A-Fa-f][0-9A-Fa-f]{0,3}):)?(0|[1-9A-Fa-f][0-9A-Fa-f]{0,3}))?::((0|[1-9A-Fa-f][0-9A-Fa-f]{0,3}):){3}|(((0|[1-9A-Fa-f][0-9A-Fa-f]{0,3}):){0,2}(0|[1-9A-Fa-f][0-9A-Fa-f]{0,3}))?::((0|[1-9A-Fa-f][0-9A-Fa-f]{0,3}):){2}|(((0|[1-9A-Fa-f][0-9A-Fa-f]{0,3}):){0,3}(0|[1-9A-Fa-f][0-9A-Fa-f]{0,3}))?::(0|[1-9A-Fa-f][0-9A-Fa-f]{0,3}):|(((0|[1-9A-Fa-f][0-9A-Fa-f]{0,3}):){0,4}(0|[1-9A-Fa-f][0-9A-Fa-f]{0,3}))?::)((0|[1-9A-Fa-f][0-9A-Fa-f]{0,3}):(0|[1-9A-Fa-f][0-9A-Fa-f]{0,3})|(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])(\.(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])){3})|(((0|[1-9A-Fa-f][0-9A-Fa-f]{0,3}):){0,5}(0|[1-9A-Fa-f][0-9A-Fa-f]{0,3}))?::(0|[1-9A-Fa-f][0-9A-Fa-f]{0,3})|(((0|[1-9A-Fa-f][0-9A-Fa-f]{0,3}):){0,6}(0|[1-9A-Fa-f][0-9A-Fa-f]{0,3}))?::)|(?!IPv6:)[0-9A-Za-z-]*[0-9A-Za-z]:[!-Z^-~]+)])'
USERNAME_REGEX = r'^[^\s\W]*([\w]+\s)*[\w]+$'
PW_REGEX = r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[#?!@$%^&*-]).{6,}$'
POSTAL_REGEX = r'^[ABCEGHJ-NPRSTVXY][0-9][ABCEGHJ-NPRSTV-Z] [0-9][ABCEGHJ-NPRSTV-Z][0-9]$'
SHIPPING_ADDRESS_REGEX = r'^[ A-Za-z0-9]+$'
POSTAL_REGEX_UPDATED = r'^(?!.*[DFIOQU])[A-VXY][0-9][A-Z] ?[0-9][A-Z][0-9]$'

'''
This file defines data models and related business logics
'''
db = SQLAlchemy(app)

#####################################################
# USER ENTITY
# Adds a "User" class and table to the database with data fields:
# username, a string of maximum length 80 characters.
# email, a string of maximum length 120 characters.
# password, a string of maximum length 30 characters.
# account_id, the foreign key of the Account entity, a unique integer key.
# Querying the User class will return username.


class User(db.Model):
    user_name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(
        db.String(120), unique=True, nullable=False,
        primary_key=True)
    password = db.Column(db.String(120),
                         nullable=False)
    postal_code = db.Column(db.String(6), unique=False, nullable=True)
    shipping_address = db.Column(db.String(100), unique=False, nullable=True)
    balance = db.Column(db.Float, unique=False, nullable=False)

    # account_id = db.Column(db.Integer,
    #                        db.ForeignKey('account.id'), nullable=False)
    # account = db.relationship('Account',
    #                           backref=db.backref('user', lazy=True))

    def __repr__(self):
        return '<User %r>' % self.email


#####################################################
# ACCOUNT ENTITY
# Adds an "Account" class and table to the database with data fields:
# id, a unique integer key.
# balance, an integer value to track money.
# pin, an integer value for user transaction verification.
# The Account id is also paired to User as account_id.
# Querying the Account class will return id.


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Integer, unique=False, nullable=False)
    pin = db.Column(db.Integer, unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.id


#####################################################
# PRODUCT ENTITY
# Adds a "Product" class and table to the database with data fields:
# product_id, a primary unique integer key.
# seller_id, a foreign key of the selling user.
# buyer_id, a foreign key of the buying user.
# title, a string value for the name of the product.
# product_price, an integer for the price of a unit of product.
# product_description, a string for the description of the product.
# quantity, an integer for how many units of product are available.


class Product(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True)
    # buyer_id = db.Column(db.Integer, db.ForeignKey(User.id))
    title = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(2000))
    quantity = db.Column(db.Integer, nullable=False)
    owner_email = db.Column(
        db.String(120),
        db.ForeignKey('user.email'),
        nullable=False)
    last_modified_date = db.Column(db.DateTime, unique=False, nullable=False)

    user = db.relationship('User',
                           backref=db.backref('product', lazy=True))

    def __repr__(self):
        return '<Product %r>' % self.product_id


#####################################################
# TRANSACTION ENTITY:
# This entity keeps track of all transactions made on the website
# Contains:
# id - Primary Key
# BuyerId   SellerId    ProductId   - Foreign Keys
# Amount    Quantity    DateAndTime - Miscellaneous data fields


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(
        db.Integer,
        db.ForeignKey('product.id'),
        nullable=False)
    # Describes amount in dollars
    price = db.Column(db.Integer, nullable=False)
    # Quantity (number) of items purchased for each ProductId
    quantity = db.Column(db.Integer)
    date = db.Column(db.DateTime)  # Date and time of the transaction
    user_email = db.Column(
        db.String(120),
        db.ForeignKey('user.email'),
        nullable=False)

    user = db.relationship('User',
                           backref=db.backref('transaction', lazy=True))
    product = db.relationship('Product',
                              backref=db.backref('transaction', lazy=True))

    def __repr__(self):
        return '<Transaction %r>' % self.transaction_id


#####################################################
# REVIEW ENTITY:
# This class keeps track of user Reviews
# Reviews can include:
# Score: A user may input a score from 1-5 or 1-10 (to be decided)
# Review: A user may input a review in the form of a string
# Reviews require:
# A verified id and user_email


class Review(db.Model):
    id = db.Column(
        db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=True)
    review = db.Column(db.String(200), unique=True, nullable=True)
    user_email = db.Column(
        db.String(120),
        db.ForeignKey('user.email'),
        nullable=False)  # link to other email

    user = db.relationship('User',
                           backref=db.backref('review', lazy=True))

    def __repr__(self):
        return '<Review %r>' % self.buyerId


# create all tables
db.create_all()


def register(name, email, password):
    '''
    Register a new user
      Parameters:
        name (string):     user name
        email (string):    user email
        password (string): user password
      Returns:
        True if registration succeeded otherwise False
    '''
    # check if both the email and password are empty
    if((len(email) == 0) or (len(password) == 0) or (len(name) == 0)):
        return False

    # check if the email follows RFC 5322
    if(len(email) <= 64):
        if(not(re.fullmatch(RFC5322_REGEX, email))):
            return False
    else:
        return False

    # check password requirements
    if(not(re.fullmatch(PW_REGEX, password))):
        return False

    # check username requirement
    if(len(name) >= 20 or len(name) < 3):
        return False

    if(not(re.fullmatch(USERNAME_REGEX, name))):
        return False

    # check if the email has been used:
    existed = User.query.filter_by(email=email).all()
    if len(existed) > 0:
        return False

    # create a new user
    user = User(
        user_name=name,
        email=email,
        password=password,
        balance=100,
        postal_code='EMPTY POSTAL',
        shipping_address='EMPTY ADDY')
    # add it to the current database session
    db.session.add(user)
    # actually save the user object
    db.session.commit()

    return True


def login(email, password):
    '''
    Check login information
      Parameters:
        email (string):    user email
        password (string): user password
      Returns:
        The user object if login succeeded otherwise None
    '''
    # check if both the email and password are empty
    if((len(email) == 0) or (len(password) == 0)):
        return False

    # check if the email follows RFC 5322
    if(len(email) <= 64):
        if(not(re.fullmatch(RFC5322_REGEX, email))):
            return False
    else:
        return False

    # check password requirements
    if(not(re.fullmatch(PW_REGEX, password))):
        return False

    valids = User.query.filter_by(email=email, password=password).all()
    if len(valids) != 1:
        return None
    return valids[0]

def updateBalance(user, balance):
    user.balance = balance
    db.session.commit()
    return True

def productOrder(product, buyerUser):
    if(product.quantity == 0):
        print("QUANTITY CHECK")
        return False
    if(buyerUser.balance < product.price):
        print("BALANCE CHECK")
        return False
    product.quantity = 0
    newBalance = buyerUser.balance - product.price
    updateBalance(buyerUser, newBalance)

    return product

def updateUserLogin(
        email,
        password,
        new_user_name,
        postalCode,
        shippingAddress):
    '''
    Check login information
      Parameters:
        email (string):    user email
        password (string): user password
        postal code : new user postal code
        shipping address: new user shipping address


      Returns:


    '''

    # check length of email and username
    if((len(email) == 0) or (len(password) == 0)):
        return False

    # regex now allows spaces
    # check shipping address requirements -> non empty alphanumeric with no
    # special characters
    if(not(re.fullmatch(SHIPPING_ADDRESS_REGEX, shippingAddress))):
        return False

    # checking that it is a valid canadian code
    if(not(re.fullmatch(POSTAL_REGEX_UPDATED, postalCode))):
        return False

    doesUserExist = User.query.filter_by(
        email=email, password=password).first()

    test = len(doesUserExist.user_name)

    if test == 0:
        print("test is zero")
        return None
        
    else:
        doesUserExist.user_name = new_user_name
        doesUserExist.postal_code = postalCode
        doesUserExist.shipping_address = shippingAddress
        print(doesUserExist.user_name)
        print(doesUserExist.shipping_address)
        print(234)
        db.session.commit()

    return doesUserExist


def createProduct(title, price, description, quantity, email,
                  date=datetime.datetime.utcnow(), id=-1):
    '''
    Add a new product
    Parameters:
    title (string):			product title
    price (int):			product price
    description (string):	product description
    price (int):			product quantity
    email (string):			user email
    date:			last_modified_date
    (optional) id:			integer primary key
    (default -1)
    Returns:
    True if product creation succeeded otherwise False
    '''
    
    # check length of title and description

    price = int(price)
    validDate = datetime.datetime(2021, 1, 2)
    invalidDate = datetime.datetime(2025, 1, 2)

    if (len(title) == 0) or (len(title) > 80) or (len(description) > 2000) or\
            (len(description) < 20) or (len(description) <= len(title)):
        print(1)
        return False

    # check title requirements (same regex as username!)
    if (not(re.fullmatch(USERNAME_REGEX, title))):
        print('REGEX CHECK')
        return False

    # check price [10, 1000]
    if (price > 10000) or (price < 10):
        print('PRICE CHECK')
        return False

    # check last_modified_date
    if (date < validDate) or (date > invalidDate):
        print('DATE CHECK')
        return False

    # check owner_email
    if (len(email) == 0):
        print('EMAIL LENGTH CHECK')
        return False

    owner = User.query.filter_by(email=email).all()

    if (len(owner) != 1):
        print('OWNER CHECK')
        return False

    products = Product.query.filter_by(
        title=title,
        owner_email=email).all()

    # if no specified id
    if id == -1:
        # check if title is in use by same user

        if len(products) != 0:
            print("PRODUCT LENGTH CHECK")
            return False

        # create a new product
        product = Product(
            title=title, price=price,
            description=description, quantity=quantity,
            owner_email=email, last_modified_date=date)
        # if product.id does not auto-increment on your
        # machine, flush previous db session!
        #
        # add it to the current database session
        db.session.add(product)
        # actually save the product object
        db.session.commit()

    else:  # specified id, updates existing product
        # check if title is in use by same user
        # if len(products) != 1:
        #     return False

        num_rows_updated = Product.query.filter_by(id=id).update(
            dict(title=title,
                 price=price,
                 description=description,
                 quantity=quantity,
                 owner_email=email,
                 last_modified_date=date))

        db.session.commit()

    return True


def updateProduct(id, title, price, description, quantity):
    '''
    Update Product Information
    Parameters:
    id (incremental int):	primary key
    title (string):			product title
    price (int):			product price
    description (string):	product description
    quantity (int):			product quantity
    Returns:
    True if update succeeded otherwise False
    '''

    # check if product_id is in use
    products = Product.query.filter_by(id=id).first()

    test = len(products.title)

    new_date = datetime.datetime.utcnow()

    if test == 0:
        return False

    # check if price is decreased
    if products.price > price:
        return False

    # update product attributes by calling createProduct
    # this ensures all product input requirements are met
    return createProduct(
        title,
        price,
        description,
        quantity,
        products.owner_email,
        new_date,
        id)
