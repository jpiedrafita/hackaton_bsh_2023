from flask import Flask, render_template, request, session, redirect, url_for, flash, g
from google.cloud import firestore
from werkzeug.security import generate_password_hash, check_password_hash
import functools

app = Flask(__name__)
# Get an instance of firestore
db = firestore.Client.from_service_account_json('./cloud-rangers-fierebase.json')

# We protect a view if we are not logged in --> g.user
# This takes a view (a view function as sign_up) and returns a function that decorates it
def require_login(view):
    # functools.wrap will map the function metadata back
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not g.user:
            return redirect(url_for('log_in'))
        return view(**kwargs)
    return wrapped_view

# Check for a user_id on the session
@app.before_request
def load_user():
    user_id = session.get('user_id')
    #debug
    print(f"user id: {user_id}")
    if user_id:
        g.user = user_id
    else:
        g.user = None

# Sign up page - Stores user and hashed password in firestore
@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():

    # Get uername and password values from the register.html form
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        # Check if user exists and populate error message
        user_check = db.collection('users').where('username', '==', username).get()
        if not username:
            error = 'Username is required'
        elif not password:
            error = 'Password is required'
        elif user_check:
            error = ('Username already taken')

        # If there are no errors we hash the password, store the new user in the db, adn redirect to log in page
        if error is None:
            password = generate_password_hash(password)
            new_user = {
            'username': username,
            'password': password
            }
            # Get a reference of the users collection
            users_ref = db.collection('users')
            users_ref.add(new_user)
            flash('User created successfully!, please log in', 'success')
            return redirect(url_for('log_in'))
        
        flash(error, 'error')

    return render_template('sign_up.html')

# Log in page - Read creentials from firestore and creates session
@app.route('/log_in', methods=['GET', 'POST'])
def log_in():
    # Get data from the login.html form
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        # We query the username in the db
        user_ref = db.collection('users').where('username', '==', username).get()

        # If the user_ref is empty then username does not exist
        if len(user_ref) == 0:
            error = 'Username or password are incorrect.'
        else:
            # if the username exists, we check hashed password
            user_data = user_ref[0].to_dict()
            stored_password = user_data.get('password')
            if not check_password_hash(stored_password, password):
                error = 'Username or password are incorrect.'
        
        # If there are no errors the user is logged in and redirect to main page
        if error is None:
            #Store user_id in session
            session.clear()
            session['user_id'] = username
            print(session['user_id'])  #debug
            return redirect('/')
        
        flash(error, 'error')

    return render_template('log_in.html')

# Log out - As long there is no log ou button use the url: app_url:5000/log_out
@app.route('/log_out', methods=['GET', 'DELETE'])
def log_out():
    session.clear()
    flash('Successfully logged out.', 'success')
    return redirect(url_for('log_in'))

# Home page
@app.route('/')
def index():
    return 'Index'


# Registered appliances page
@app.route('/appliances')
@require_login
def appliances():
    # Get user ID
    user = session.get('user_id')
    # Ger user appliances
    appliances_ref = db.collection('user_appliances').where('user', '==', user)
    appliances = [doc.to_dict() for doc in appliances_ref.get()]
    
    return render_template('appliances.html', appliances=appliances)

# Register new appliance
@app.route('/appliances/new', methods=['GET', 'POST'])
@require_login
def appliance_create():
    if request.method == 'POST':
        # TODO: update the form with appliances data
        brand = request.form['brand']
        model = request.form['model']
        # ...
        error = None

        if not model:
            error = 'Model is required.'

        if error is None:
            # TODO: instantiate appliance full data
            new_appliance = {
                'brand': brand,
                'model': model
                # ...
            }
             # Get a reference of the users collection
            appliances_ref = db.collection('user_appliances')
            appliances_ref.add(new_appliance)
            flash(f"Appliance {model} successfully registered!", 'success')
            return redirect(url_for('appliances'))
        
        flash(error, 'error')
    
    return render_template('appliance_create.html')

if __name__ == '__main__':
    app.secret_key = 'test1234'  # Set a secret key for flash messages
    app.run()
