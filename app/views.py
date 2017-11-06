from flask import render_template, flash, redirect, request, session, escape, url_for
from app import app, DBSession
from .form import LoginForm, RegisterForm
from .dao import Person


@app.route('/')
@app.route('/index')
def index():
    if 'username' in session:
        user = {'nickname': escape(session['username'])}
    else:
        return 'you are not login in'
    posts = [  # fake array of posts
        {
            'author': {'nickname': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'nickname': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', user=user, posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # u = User(form.username.data, form.password.data)
    if form.validate_on_submit():
        if select_db(form.username.data, form.password.data):
            session['username'] = form.username.data
            return redirect('/index')
        else:
            return 'login failed'
    return render_template('login.html', title='sign in', form=form, providers=app.config['OPENID_PROVIDERS'])


@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('you were logout')
    return redirect(url_for('login'))


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    session = DBSession()
    # request.form['username'] ---> POST
    # request.args.get('username','') ---> GET
    new_person = Person(name=form.username.data, password=form.password.data, email=form.email.data)
    if form.validate_on_submit():
        session.add(new_person)
        session.commit()
        session.close()
        return redirect('/login')
    return render_template('register.html', title='register', form=form)


def select_db(username, pword):
    # cursor = mysql.connect().cursor()
    # cursor.execute('SELECT * from t_user where name=%s and password=%s', (username, pword))
    # data = cursor.fetchone()
    session = DBSession()
    user = session.query(Person).filter(Person.name == username, Person.password == pword).one()
    if user is None:
        return False
    else:
        return True

# class User:
#     def __init__(self, name, password):
#         self.name = name
#         self.password = password
