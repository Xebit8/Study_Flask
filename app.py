from flask import Flask, render_template, request, redirect, url_for, session
from sqlalchemy.exc import IntegrityError
from models import add_user, check_user

app = Flask(__name__)
app.secret_key = 'themostsecretkeyinthealluniversecreatedbymeonthelessonwithpks22'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        password_check = request.form['password_check']
        if password_check != password:
            return render_template('index.html', error="passwords_not_match")
        try:
            add_user(name, email, password)
        except IntegrityError:
            return render_template('index.html', error="already_exists")
        session['username'] = name
        return redirect(url_for('user_page', name=name))
    return render_template('index.html')

@app.route('/users/<name>')
def user_page(name):
    return render_template('user.html', username=name)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = check_user(email, password)
        if user:
            session['username'] = user.name
            return redirect(url_for('user_page', name=user.name))
        else:
            return render_template('login.html', error=True) # начать с добавления в юзер.хтмл
    return render_template('login.html')

app.run(debug=True) #app.run('0.0.0.0','3000')