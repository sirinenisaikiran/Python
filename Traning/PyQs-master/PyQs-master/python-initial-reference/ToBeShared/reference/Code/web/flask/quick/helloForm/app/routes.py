from flask import *
from app import app
from app.forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
    user = {'username':'Nobody'}
    if session.get('logged_in'):
        user = {'username': session.get('logged_in')}
    return render_template('index.html', title='Home', user=user) #Jinja2 template engine

    
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(form.username.data, form.remember_me.data))
        #Check db or something 
        session['logged_in'] = form.username.data
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

'''
#If flask-wtf is not used, use as 

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

'''