from flask import render_template, redirect, url_for, flash, request, abort
from communitywebsite import app, database, bcrypt
from communitywebsite.forms import FormLogin, FormCreateAccount, FormEditProfile, FormCreatePost
from communitywebsite.models import Customer, Post
from flask_login import login_user, logout_user, current_user, login_required
import secrets
import os
from PIL import Image


@app.route('/')
def home():
    posts = Post.query.order_by(Post.id.desc())
    return render_template('home.html', posts=posts)


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/users')
@login_required
def users():
    user_list = Customer.query.all()
    return render_template('users.html', user_list=user_list)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    form_create_account = FormCreateAccount()
    if form_login.validate_on_submit() and 'login_submit_button' in request.form:
        user = Customer.query.filter_by(email=form_login.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form_login.password.data):
            login_user(user, remember=form_login.data_remember.data)
            flash(f'Sucsessful Login! e-Mail: {form_login.email.data}', 'alert-success')
            parameter_next = request.args.get('next')
            if parameter_next:
                return redirect(parameter_next)
            else:
                return redirect(url_for('home'))
        else:
            flash(f'Login Fail. Wrong user or password', 'alert-danger')
    if form_create_account.validate_on_submit() and 'create_button_submit' in request.form:
        password_crypt = bcrypt.generate_password_hash(form_create_account.password.data)
        user = Customer(username=form_create_account.username.data, email=form_create_account.email.data, password=password_crypt)
        database.session.add(user)
        database.session.commit()
        flash(f'Account Created for e-Mail: {form_create_account.email.data}', 'alert-success')
        return redirect(url_for('home'))
    return render_template('login.html', form_login=form_login, form_create_account=form_create_account)


@app.route('/exit')
@login_required
def get_out():
    logout_user()
    flash('Bye Bye ! See you soon', 'alert-success')
    return redirect(url_for('home'))


@app.route('/profile')
@login_required
def profile():
    user_picture = url_for('static', filename='Profile_Pictures/{}'.format(current_user.user_picture))
    return render_template('profile.html', user_picture=user_picture)


@app.route('/post/create', methods=['GET', 'POST'])
@login_required
def post_create():
    form = FormCreatePost()
    if form.validate_on_submit():
        post = Post(title=form.title.data, body=form.body.data, author=current_user)
        database.session.add(post)
        database.session.commit()
        flash('Post Created Successfully', 'alert-success')
        return redirect(url_for('home'))
    return render_template('post_creation.html', form=form)


def save_image(image):
    img_cod = secrets.token_hex(8)
    name, extension = os.path.splitext(image.filename)
    file_name = name + img_cod + extension
    complete_path = os.path.join(app.root_path, 'static/Profile_Pictures', file_name)
    size = (155, 155)
    reduced_img = Image.open(image)
    reduced_img.thumbnail(size)
    reduced_img.save(complete_path)
    return file_name


def update_courses(form):
    course_lst = []
    for field in form:
        if 'class_' in field.name:
            if field.data:
                course_lst.append(field.label.text)
    return ';'.join(course_lst)


@app.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = FormEditProfile()
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.username = form.username.data
        if form.user_picture.data:
            image = save_image(form.user_picture.data)
            current_user.user_picture = image
        current_user.courses = update_courses(form)
        database.session.commit()
        flash(f'Profile Updated !', 'alert-success')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.username.data = current_user.username
    user_picture = url_for('static', filename='Profile_Pictures/{}'.format(current_user.user_picture))
    return render_template('editprofile.html', user_picture=user_picture, form=form)


@app.route('/post/<post_id>', methods=['GET', 'POST'])
@login_required
def show_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.author:
        form = FormCreatePost()
        if request.method == 'GET':
            form.title.data = post.title
            form.body.data = post.body
        elif form.validate_on_submit():
            post.title = form.title.data
            post.body = form.body.data
            database.session.commit()
            flash('Post Updated Successfully', 'alert-success')
            return redirect(url_for('home'))
    else:
        form = None
    return render_template('post.html', post=post, form=form)


@app.route('/post/<post_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.author:
        database.session.delete(post)
        database.session.commit()
        flash('Post Excluded Successfully !', 'alert-danger')
        return redirect(url_for('home'))
    else:
        abort(403)
