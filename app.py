from flask import Flask, render_template, request, session, redirect, url_for, flash
from google.cloud import firestore
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
# Get an instance of firestore
db = firestore.Client.from_service_account_json('./cloud-rangers-fierebase.json')

# Home page
@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    # Get uername and password values from the register.html form
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        # Check if user exists
        user_check = db.collection('users').where('username', '==', username).get()

        if not username:
            error = 'Username is required'
        elif not password:
            error = 'Password is required'
        elif user_check:
            error = ('Username already taken')

        # If there are no errors we hash the password and store the new user in the db
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
            return redirect(url_for('login'))
        
        flash(error, 'error')

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():

    # Get data from the login.html form
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        # We query the username in the db
        user = db.collection('users').where('username', '==', username).get()

        if not user or not check_password_hash(user.password, password):
            error = 'Username or password are incorrect.'
        
        if error is None:
            session.clear()
            session['user_id'] = user.id
            print(user.id)
            return redirect(url_for('home'))

        flash(error, 'error')

    return render_template('login.html')

@app.route('/logout', methods=['GET', 'DELETE'])
def logout():
    session.clear()
    flash('Successfully logged out.', 'success')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.secret_key = 'test1234'  # Set a secret key for flash messages
    app.run()
