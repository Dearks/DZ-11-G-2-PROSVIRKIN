from app.setup import db
import hashlib, datetime, os

class User(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    name = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(30), nullable=False)
    date_of_registration = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    def validate(self, password):
        return self.password == hashlib.md5(password.encode("utf8")).hexdigest()

    def set_password(self, password):
        self.password = hashlib.md5(password.encode('utf8')).hexdigest()

class Sofa(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(2000), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    url = db.Column(db.String(200), nullable=False) 

    def __repr__(self):
        return f'{self.name}'    

    def dec_amount(self, amount):
        self.amount -= amount


class ShoppingCart(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    product_name = db.Column(db.Integer, db.ForeignKey(Sofa.id), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    is_visible = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'{self.product_name}'
    
    def inc_amount(self, amount):
        self.quantity += amount

    def dec_amount(self, amount):
        self.quantity -= amount
    
    def update_visibility(self):
        self.is_visible = False

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    text = db.Column(db.Text)

def start_db():
    sofa1 = Sofa(
        name='Tango',
        description='Tango. Восхитительный диван для уставших после рабочего дня людей.',
        price='10000',
        amount=100,
        url='IMG_4198.JPG'
    )
    sofa2 = Sofa(
        name='Dolphin',
        description='Dolphin. Восхитительнее, чем Tango.',
        price='20000',
        amount=100,
        url='IMG_4199.JPG'
    )
    sofa3 = Sofa(
        name='Conrad',
        description='Conrad. Самый элитный из диванов.',
        price='30000',
        amount=100,
        url='IMG_4200.JPG'
    )

    review1 = Review(
        name='chad',
        email='chad@chad.ru',
        text='Отличные диваны! Сижу на них послу каждой тренировки, отлично расслабляет.'
    )

    db.session.add(sofa1)
    db.session.add(sofa2)
    db.session.add(sofa3)
    db.session.add(review1)

    if len(list(User.query.all())) == 0:
        dummy = User(
                    name='anthony',
                    password=''
                )
        dummy.set_password('anthony')
        db.session.add(dummy) 

    db.session.commit()

def create_db():
    db.create_all()

def get_sofa_by_url(name):
    return Sofa.query.filter(Sofa.name == name).one()

def get_sofa_id_by_url(name):
    return Sofa.query.filter(Sofa.name == name).one().id

def get_sofas():
    return Sofa.query.all()

def get_reviews():  
    return Review.query.all()

def get_cart_for_user(user_id):
    return ShoppingCart.query.filter(User.id == user_id)

def disable_cart_for_user(user_id):
    cart = get_cart_for_user(user_id)
    for cart_item in cart:
        cart_item.update_visibility()
        db.session.add(cart_item)
    db.session.commit()

def get_total_price_for_user(user_id):
    cart = get_cart_for_user(user_id)
    total_price = 0
    for cart_item in cart:
        if cart_item.is_visible:
            total_price += cart_item.quantity * cart_item.price
    return total_price
