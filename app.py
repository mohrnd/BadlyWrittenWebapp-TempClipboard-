from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import database
import config
import dynamoDB  # Import the DynamoDB functions

app = Flask(__name__)
app.secret_key = config.SECRET_KEY

@app.route('/', methods=['GET', 'POST'])
def login():
    if 'email' in session:
        return redirect(url_for('home'))
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = database.load_user_by_email(email)
        if user and check_password_hash(user['password'], password):
            session['email'] = email
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'email' in session:
        return redirect(url_for('home'))
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if database.load_user_by_email(email):
            flash('Email already exists. Please choose a different one.', 'danger')
        elif password != confirm_password:
            flash('Passwords do not match. Please try again.', 'danger')
        else:
            hashed_password = generate_password_hash(password)
            database.add_user(email, hashed_password)
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/home')
def home():
    if 'email' not in session:
        return redirect(url_for('login'))
    return render_template('home.html')

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('login'))

@app.route('/share', methods=['POST'])
def share():
    if 'email' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    data = request.json
    code = data.get('code')
    content = data.get('content')
    if code and content:
        user_id = session['email']  # Use email as a user ID
        dynamoDB.write_to_dynamodb(code, user_id, content)
        return jsonify({'message': 'Content shared successfully'}), 200
    return jsonify({'error': 'Invalid input'}), 400

@app.route('/view/<code>', methods=['GET'])
def view(code):
    item = dynamoDB.read_from_dynamodb(code)
    if item:
        return jsonify({'content': item['content']})
    return jsonify({'error': 'Content not found or expired'}), 404

if __name__ == '__main__':
    app.run(debug=True)


