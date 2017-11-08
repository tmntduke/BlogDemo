from flask import render_template, flash, redirect, request, session, escape, url_for
from app import app, DBSession
from .form import LoginForm, RegisterForm, EditForm
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


@app.route('/user/<username>')
def user(username):
    user = select_user(username)
    if user is None:
        return 'user is none'

    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]

    return render_template('user.html', user=user, posts=posts)


@app.route('/edit', methods=['GET', 'POST'])
def edit():
    form = EditForm()
    if 'username' in session:
        current = session['username']
        if form.validate_on_submit():
            nickname = form.nickname.data
            about_me = form.about_me.data
            update_about(current, nickname, about_me)
            session['username'] = nickname
            flash('Your changes have been saved.')
            return redirect(url_for('index'))
    else:
        return 'you are not login in'
    return render_template('edit.html', form=form)


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


@app.errorhandler(404)
def internal_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    session = DBSession()
    session.rollback()
    return render_template('500.html'), 500


def update_about(current, nickname, about):
    print(current)
    session = DBSession()
    user = session.query(Person).filter(Person.name == current).one()
    user.name = nickname
    user.about = about
    session.add(user)
    session.commit()


def select_user(username):
    session = DBSession()
    user = session.query(Person).filter(Person.name == username).one()
    return user

# class User:
#     def __init__(self, name, password):
#         self.name = name
#         self.password = password
