from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ksorm.db'
db = SQLAlchemy(app)



class people_log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(80), nullable=True)
    login = db.Column(db.String(80), nullable=True)
    password = db.Column(db.String(80), nullable=True)
    payment = db.Column(db.String(80), nullable=True)
    name = db.Column(db.String(80), nullable=True)
    dateofbirthday = db.Column(db.String(80), nullable=True)
    mail = db.Column(db.String(80), nullable=True)
    adress = db.Column(db.String(80), nullable=True)



class Catalog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=True)
    description_short = db.Column(db.String(80), nullable=True)
    description_full = db.Column(db.String(80), nullable=True)
    description_video = db.Column(db.String(80), nullable=True)


class Items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Catalog_id = db.Column(db.Integer, db.ForeignKey('catalog.id'), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(80), nullable=False)
    photo = db.Column(db.String(80), nullable=True)
    Catalog = db.relationship('catalog',
                               backref=db.backref('item', lazy=False))


class Shopping_cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('people_log.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    count = db.Column(db.Integer, nullable=False)
    customer = db.relationship('people_log',
                            backref=db.backref('Shopping_cart', lazy=False))
    item = db.relationship('Items',
                              backref=db.backref('Shopping_cart', lazy=False))


class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('people_log.id'), nullable=False)
    date = db.Column(db.String(80), nullable=False)
    total = db.Column(db.Integer, nullable=False)
    customer = db.relationship('people_log',
                            backref=db.backref('order', lazy=False))

    
class Order_list(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    priceperitem = db.Column(db.Integer, nullable=False)
    count = db.Column(db.Integer, nullable=False)

db.create_all()