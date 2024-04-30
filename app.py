from flask import Flask, render_template, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime

today = datetime.today().strftime('%Y-%m-%d')

import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost/shop'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = True
app.config['UPLOAD_FOLDER'] = 'static/img'
app.config['SECRET_KEY'] = 'aaaa'
db = SQLAlchemy(app)
ALLOWED_EXTESION = {'png', 'jpg', 'jpeg'}


class Users(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String)
    number = Column(String)
    gmail = Column(String)
    password = Column(String)
    photo = Column(String)
    admin = Column(Boolean)


class News(db.Model):
    id = Column(Integer, primary_key=True)
    news_name = Column(String)
    news_data = Column(String)
    news_text = Column(String)


class Product(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String)
    prise = Column(String)
    about = Column(String)
    photo = Column(String)


with app.app_context():
    db.create_all()


def current_user():
    user_now = None
    if 'username' in session:
        user_get = Users.query.filter(Users.name == session['username']).first()
        user_now = user_get

    return user_now


def users_folder():
    upload_folder = 'static/img/'
    return upload_folder


def checkFile(filename):
    value = '.' in filename
    type_file = filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTESION
    return value and type_file


@app.route('/')
def hello_world():  # put application's code here
    user = current_user()
    return render_template('menu.html', user=user)


@app.route('/katalog', methods=["POST", "GET"])
def katalog():  # put application's code here

    user = current_user()
    if request.method == "POST":
        name = request.form.get('name')
        about = request.form.get('about')
        prise = request.form.get('prise')
        photo = request.form.get('photo')
        add = Product(name=name, prise=prise, about=about, photo=photo)
        db.session.add(add)
        db.session.commit()
        return redirect(url_for('katalog'))
    katalog = Product.query.all()
    return render_template('katalog.html', user=user, katalog=katalog)


@app.route('/header')
def header():  # put application's code here
    user = current_user()
    return render_template('header.html', user=user)


@app.route('/profile', methods=["POST", "GET"])
def profile():
    user = current_user()
    if request.method == "POST":
        name = request.form.get('name')
        number = request.form.get('nomer')
        gmail = request.form.get('gmail')
        password = request.form.get('password')
        hashed = generate_password_hash(password=password, method='sha256')
        Users.query.filter(Users.id == user.id).update({
            "name": name,
            "number": number,
            "password": hashed,
            "gmail": gmail
        })
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('profile.html', user=user)


@app.route('/logout')
def logout():
    session['username'] = ""
    return redirect(url_for('hello_world'))


@app.route('/news', methods=["POST", "GET"])
def news():
    user = current_user()
    if request.method == "POST":
        name = request.form.get('name')
        news = request.form.get('text')
        add = News(news_name=name, news_data=today, news_text=news)
        db.session.add(add)
        db.session.commit()
        return redirect(url_for('news'))
    news = News.query.all()
    return render_template('novosti.html', user=user, news=news)


@app.route('/korzina')
def korzina():
    user = current_user()
    return render_template('korzina.html', user=user)


@app.route('/lichniy', methods=["POST", "GET"])
def lich():
    user = current_user()
    if request.method == "POST":
        name = request.form.get('name')
        gmail = request.form.get('gmail')
        number = request.form.get('nomer')
        password = request.form.get('password')
        photo = request.files['rasm']
        folder = users_folder()
        if photo and checkFile(photo.filename):
            photo_file = secure_filename(photo.filename)
            photo_url = '/' + folder + photo_file
            app.config['UPLOAD_FOLDER'] = folder
            photo.save(os.path.join(app.config["UPLOAD_FOLDER"], photo_file))
        hashed = generate_password_hash(password=password, method='sha256')
        add = Users(name=name, number=number, gmail=gmail, password=hashed, photo=photo_url)
        db.session.add(add)
        db.session.commit()
        return redirect(url_for('lich'))
    return render_template('lich.html', user=user)


@app.route('/ofor')
def ofor():
    user = current_user()
    return render_template('ofor.html', user=user)


@app.route('/tovar')
def tovar():
    user = current_user()
    return render_template('tovara.html', user=user)


@app.route('/login', methods=['POST', 'GET'])
def login():
    user = current_user()
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')
        username = Users.query.filter(Users.name == name).first()
        if username:
            if check_password_hash(username.password, password):
                session["username"] = username.name
                return redirect(url_for('hello_world'))
            else:
                return render_template('login.html', error='Username or password incorect')
    return render_template('login.html', user=user)


@app.route('/delete/<int:product_id>')
def delete(product_id):
    filter = Product.query.filter(Product.id == product_id).delete()
    db.session.commit()
    return redirect(url_for("katalog"))


@app.route('/deletes/<int:product_id>')
def deletes(product_id):
    filter = News.query.filter(News.id == product_id).delete()
    db.session.commit()
    return redirect(url_for("news "))


@app.route('/edit/<int:product_id>', methods=["POST", "GET"])
def edit(product_id):
    return render_template('edit.html', edit=product_id)


@app.route('/edit_new/<int:news_id>', methods=["POST", "GET"])
def edit_new(news_id):
    return render_template('edit_new.html', edit=news_id)


@app.route('/edite_new/<int:id>', methods=["POST", "GET"])
def edite_new(id):
    if request.method == "POST":
        name = request.form.get('name')
        prise = request.form.get('prise')
        about = request.form.get('about')
        News.query.filter(News.id == id).update({
            "news_name": name,
            "news_data": prise,
            "news_text": about,

        })
        db.session.commit()
    return redirect(url_for('news'))


@app.route('/edite/<int:id>', methods=["POST", "GET"])
def edite(id):
    if request.method == "POST":
        name = request.form.get('name')
        prise = request.form.get('prise')
        about = request.form.get('about')
        photo = request.form.get('photo')
        Product.query.filter(Product.id == id).update({
            "name": name,
            "prise": prise,
            "about": about,
            "photo": photo
        })
        db.session.commit()
    return redirect(url_for('katalog'))
