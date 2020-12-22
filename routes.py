import os
import random
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort, session
from app import app, db, bcrypt
from app.forms import RegistrationFormCustomer, RegistrationFormFoodseller, LoginForm, UpdateCustomerAccountForm, UpdateFoodsellerAccountForm, PostForm
from app.models import Customer, Foodseller, Post
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
        flash('Account created for %s , you can login now' % form.foodsellerName.data)
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
        flash('Account created for %s , you can login now' % form.username.data)
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
        posts = Post.query.all()
        return render_template('customerPage.html',posts=posts)
    else:
        return redirect(url_for('login'))

@app.route('/foodsellerPage')
def foodsellerPage():
    if session['type'] == "customer":
        return redirect(url_for('customerPage'))
    elif session['type'] == "foodseller":
        return render_template('foodsellerPage.html')
    else:
        return redirect(url_for('login'))

@app.route('/post/new', methods=['GET','POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Post created!')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')

@app.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@app.route('/post/<int:post_id>/update',methods=['GET','POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    else:
        form = PostForm()
        if form.validate_on_submit():
            post.title = form.title.data
            post.content = form.content.data
            db.session.commit()
            flash('Post updated!')
            return redirect(url_for('post', post_id=post.id))
        elif request.method == 'GET':
            form.title.data = post.title
            form.content.data = post.content
        return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')

@app.route('/post/<int:post_id>/delete',methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted!')
    return redirect(url_for('customerPage'))
