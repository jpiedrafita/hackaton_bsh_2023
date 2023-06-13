from flask import Flask, render_template, request, redirect, url_for, flash
from google.cloud import firestore
from werkzeug.security import generate_password_hash


app = Flask(__name__)
# Get an instance of firestore
db = firestore.Client.from_service_account_json('./prj-sb-multicloudpoc2f-73fde790ff5f.json')

@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    # Get data from the register.html form
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        # Check if user exists
        user_check= db.collection('users').where('username', '==', username).get()

        if not username:
            error = 'Username is required'
        elif not password:
            error = 'Password is required'
        elif user_check:
            error = ('Username already taken')

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
    return render_template('login.html')

if __name__ == '__main__':
    app.secret_key = 'test1234'  # Set a secret key for flash messages
    app.run()
