import os
import random
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort, session
from app import app, db, bcrypt
from app.forms import RegistrationFormCustomer, RegistrationFormFoodseller, LoginForm, UpdateCustomerAccountForm, UpdateFoodsellerAccountForm, OfferForm
from app.models import Customer, Foodseller, Offer
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html',title='home')

@app.route('/registerFoodseller',methods=['GET','POST'])
def registerFoodseller():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationFormFoodseller()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data.decode('utf-8'))
        register = Foodseller(foodsellerName=form.foodsellerName.data,
                              email=form.email.data,
                              city=form.city.data,
                              address=form.address.data,
                              phone_number=form.phone_number.data,
                              password=hashed_password)
        db.session.add(register)
        db.session.commit()
        flash('Account created for %s' % form.foodsellerName.data)
        return redirect(url_for('login'))
    return render_template('registerFoodseller.html', title='Register', form=form)

@app.route('/registerCustomer',methods=['GET','POST'])
def registerCustomer():
    if current_user.is_authenticated:
        return redirect(url_for('customerPage'))
    form = RegistrationFormCustomer()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data.decode('utf-8'))
        register = Customer(username=form.username.data,
                            name=form.name.data,
                            surname=form.surname.data,
                            email=form.email.data,
                            password=hashed_password)
        db.session.add(register)
        db.session.commit()
        flash('Account created for %s' % form.username.data)
        return redirect(url_for('login'))
    return render_template('registerCustomer.html', title='Register', form=form)

@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        if session['type'] == 'customer':
            return redirect(url_for('customerPage'))
        else:
            return redirect(url_for('foodsellerPage'))

    form = LoginForm()
    if form.validate_on_submit():
        user = Customer.query.filter_by(email=form.email.data).first()
        session['type'] = 'customer'
        if user is None:
            user = Foodseller.query.filter_by(email=form.email.data).first()
            session['type'] = 'foodseller'
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            if session['type'] == 'foodseller':
                return redirect(url_for('foodsellerPage'))
            else:
                return redirect(url_for('customerPage'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_number = random.randint(0, 16777215)
    hex_number = str(hex(random_number))
    hex_number = '#' + hex_number[2:]
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = hex_number + f_ext
    picture_path = os.path.join(app.root_path, 'static/pictures', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route('/customerAccount',methods=['GET','POST'])
@login_required
def customerAccount():
    form = UpdateCustomerAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.name = form.name.data
        current_user.surname = form.surname.data
        db.session.commit()
        flash('Account updated')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.name.data = current_user.name
        form.surname.data = current_user.surname
    image_file = url_for('static', filename='pictures/' + current_user.image_file)
    return render_template('customerAccount.html', title='Account', image_file=image_file, form=form)

@app.route('/foodsellerAccount',methods=['GET','POST'])
@login_required
def foodsellerAccount():
    form = UpdateFoodsellerAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.foodsellerName = form.foodsellerName.data
        current_user.email = form.email.data
        current_user.city = form.city.data
        current_user.address = form.address.data
        current_user.phone_number = form.phone_number.data
        db.session.commit()
        flash('Account updated')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.foodsellerName.data = current_user.foodsellerName
        form.email.data = current_user.email
        form.city.data = current_user.city
        form.address.data = current_user.address
        form.phone_number.data = current_user.phone_number
    image_file = url_for('static', filename='pictures/' + current_user.image_file)
    return render_template('foodsellerAccount.html', title='Account', image_file=image_file, form=form)

@app.route('/customerPage')
def customerPage():
    if session['type'] == "foodseller":
        return redirect(url_for('foodsellerPage'))
    elif session['type'] == "customer":
        return render_template('customerPage.html')
    else:
        return redirect(url_for('login'))

@app.route('/foodsellerPage')
def foodsellerPage():
    if session['type'] == "customer":
        return redirect(url_for('customerPage'))
    elif session['type'] == "foodseller":
        offers = Offer.query.all()
        return render_template('foodsellerPage.html', offers=offers)
    else:
        return redirect(url_for('login'))

@app.route('/offer/new', methods=['GET','POST'])
@login_required
def new_offer():
    form = OfferForm()
    if form.validate_on_submit():
        offer = Offer(offer_name=form.offer_name.data, brand=form.brand.data, description=form.description.data, exp_date=form.exp_date.data, price=form.price.data, percentage_discount=form.percentage_discount.data, seller=current_user)
        db.session.add(offer)
        db.session.commit()
        flash('Offer created!')
        return redirect(url_for('foodsellerPage'))
    return render_template('create_offer.html', title='New Offer', form=form, legend='New Offer')

@app.route('/offer/<int:offer_id>')
def offer(offer_id):
    offer = Offer.query.get_or_404(offer_id)
    return render_template('offer.html', offer_name=offer.offer_name, offer=offer)

@app.route('/offer/<int:offer_id>/update',methods=['GET','POST'])
@login_required
def update_offer(offer_id):
    offer = Offer.query.get_or_404(offer_id)
    if offer.seller != current_user:
        abort(403)
    else:
        form = OfferForm()
        if form.validate_on_submit():
            offer.offer_name = form.offer_name.data
            offer.brand = form.brand.data
            offer.description = form.description.data
            offer.exp_date = form.exp_date.data
            offer.price = form.price.data
            offer.percentage_discount = form.percentage_discount.data
            db.session.commit()
            flash('Offer updated!')
            return redirect(url_for('offer', offer_id=offer.id))
        elif request.method == 'GET':
            form.offer_name.data = offer.offer_name
            form.brand.data = offer.brand
            form.description.data = offer.description
            form.exp_date.data = offer.exp_date
            form.price.data = offer.price
            form.percentage_discount.data = offer.percentage_discount
        return render_template('create_offer.html', title='Update Offer', form=form, legend='Update Offer')

@app.route('/offer/<int:offer_id>/delete',methods=['POST'])
@login_required
def delete_offer(offer_id):
    offer = Offer.query.get_or_404(offer_id)
    if offer.seller != current_user:
        abort(403)
    db.session.delete(offer)
    db.session.commit()
    flash('Offer deleted!')
    return redirect(url_for('foodsellerPage'))
