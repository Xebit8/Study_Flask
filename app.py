import datetime
from flask import (Flask, render_template, request, redirect, 
                  url_for, session, flash)
from sqlalchemy.exc import IntegrityError
from models import (add_user, check_user, add_task, get_user_tasks, 
                    delete_task, change_task)


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

@app.route('/users/<name>', methods=['GET', 'POST'])
def user_page(name):
    if request.method == 'POST':
        title = request.form['title']
        details = request.form['details']
        deadline_date = request.form['deadline_date']
        print(deadline_date)
        add_task(session['username'], title, details, deadline_date)
    user_tasks = get_user_tasks(name)
    return render_template('user.html', username=name, tasks=user_tasks)

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

@app.route('/logout')
def logout():
    # del session['username'] # рискованно
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/remove/<task_id>')
def delete_tasks(task_id):
    delete_task(session['username'], task_id)
    flash(f"{task_id} was deleted")
    return redirect(url_for('user_page', name=session['username']))

@app.route('/status/task_<task_id>')
def change_tasks(task_id):
    change_task(session['username'], task_id)
    flash(f"Status of {task_id} was changed")
    return redirect(url_for('user_page', name=session['username']))

app.run(debug=True) #app.run('0.0.0.0','3000')