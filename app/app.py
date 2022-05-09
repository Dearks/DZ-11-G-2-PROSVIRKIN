from app.models import *
from app.setup import *
import sqlalchemy

@app.route('/')
def setup():
    return redirect('/index')

@app.route('/index')
def code():
    return render_template('index.html')

@app.route('/about_us')
def about_us():
    return render_template('about_us.html')

@app.route('/items/<sofa>', methods=['GET', 'POST'])
def render_sofa(sofa):
    if request.method == 'POST':
        if session.get('login') is not None:
            user = User.query.filter(User.name==session.get('login')).one()
            product = get_sofa_by_url(sofa)
            if user:
                quantity = request.form.get('quantity')
                if get_sofa_by_url(sofa).amount >= int(quantity):
                    cartitem = None
                    try:
                        cartitem = ShoppingCart.query.filter(sqlalchemy.and_(ShoppingCart.product_name==product.name, ShoppingCart.is_visible==True)).one()
                        cartitem.inc_amount(int(quantity))
                    except sqlalchemy.exc.NoResultFound:
                        cartitem = ShoppingCart(
                            user_id=user.id,
                            product_name=product.name,
                            price=product.price,
                            quantity=quantity
                        )

                    product.dec_amount(int(quantity))
                    db.session.add(cartitem)
                    db.session.commit()

                    flash('Товар добавлен в корзину', 'success')
                else:
                    flash('Недостаточно товара на складe', 'warning')
                    
            return render_template("sofa.html", item=get_sofa_by_url(sofa))

        flash('Пожалуйста, войдите в свой аккаунт, чтобы продолжить', 'warning')
    return render_template("sofa.html", item=get_sofa_by_url(sofa))

@app.route('/<login>', methods=['GET', 'POST'])
def render_profile(login):
    if session.get('login') == login:
        user = User.query.filter(User.name == login).one()
        if request.method == 'POST':
            old_password = request.form.get('old_password')
            new_password = request.form.get('new_password')

            if old_password:
                if user.validate(old_password):
                    user.set_password(new_password)
                    flash('Пароль изменен', 'success')
                    db.session.add(user)
                    db.session.commit()
                elif new_password == None:
                    flash('Новый пароль пуст', 'warning')
                else:
                    flash('Старый пароль неверен', 'warning')
        return render_template('profile.html', user=user, cart=get_cart_for_user(user.id), total_price=get_total_price_for_user(user.id))
        
    flash('Пожалуйста, войдите в свой аккаунт, чтобы продолжить', 'warning')
    return redirect('/login', code=301)

@app.route('/login', methods=["GET", "POST"])
def render_login():
    if request.method == "POST":
        login = request.form.get("login")
        password = request.form.get("password")
        try:
            if User.query.filter(User.name == login).one().validate(password):
                session["login"] = login
                return redirect('/', code=301)
            flash("Неправильный логин или пароль", "warning")
        except sqlalchemy.exc.NoResultFound:
            flash("Неправильный логин или пароль", "warning")
    return render_template('login.html')

@app.route("/proceed_payment/<login>", methods=["POST", "GET"])
def proceed_payment(login):
    if session.get('login') == login:
        user = User.query.filter(User.name == session.get('login')).one()
        
        disable_cart_for_user(user.id)
    
        flash('Спасибо за покупку!', 'success')   

    return redirect('/catalog')

@app.route("/logout")
def render_logout():
    if session.get("login"):
        session.pop("login")
        flash("Вы вышли из аккаунта", "success")
    return redirect("/", code=302)

@app.route('/catalog')
def catalog():
    sofas = Sofa.query.all()
    return render_template('catalog.html', items=sofas)

@app.route('/reviews', methods=["POST", "GET"])
def reviews():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        text = request.form.get("feedback")
        print(name, email, text)
        if name != "" and (email.index('@') < email.rfind('.')) and email.count('@') == 1 and text != "":
            feedback = Reviews(name=name,
                             email=email,
                             text=text)
            db.session.add(feedback)
            db.session.commit()
        else:
            flash('Пожалуйста, проверьте правильность заполненных полей', 'warning')
    feedback = Review.query.all()
    return render_template('feedback.html', feedback=feedback)


