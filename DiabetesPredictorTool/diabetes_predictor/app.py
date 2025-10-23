import os
import pickle
import logging
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from diabetes_predictor.model import predict_diabetes, create_and_save_model
from diabetes_predictor.utils import is_valid_email, is_strong_password

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "development-secret-key")

# In-memory user database for demo (use real DB in production)
users = {}

# Load or create model
model_path = os.path.join(os.path.dirname(__file__), 'model.pkl')
try:
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    logging.info("Model loaded successfully")
except FileNotFoundError:
    model = create_and_save_model()
    logging.info("Model created and saved")

# Initialize database
def init_db():
    conn = sqlite3.connect('app.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            pregnancies INTEGER,
            glucose REAL,
            blood_pressure REAL,
            skin_thickness REAL,
            insulin REAL,
            bmi REAL,
            diabetes_pedigree REAL,
            age INTEGER,
            result TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Call init_db on startup
init_db()

# Check login
def is_logged_in():
    return 'user_id' in session

@app.route('/')
def index():
    return redirect(url_for('home') if is_logged_in() else url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = request.form.get('remember') == 'on'

        if email in users and check_password_hash(users[email]['password'], password):
            session['user_id'] = email
            session['username'] = users[email]['username']
            if remember:
                session.permanent = True
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password.', 'danger')

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not all([username, email, password, confirm_password]):
            flash('All fields are required!', 'danger')
        elif not is_valid_email(email):
            flash('Enter a valid email address!', 'danger')
        elif not is_strong_password(password):
            flash('Password must be at least 8 chars and include upper, lower, and numbers!', 'danger')
        elif password != confirm_password:
            flash('Passwords do not match!', 'danger')
        elif email in users:
            flash('Email already registered!', 'danger')
        else:
            users[email] = {
                'username': username,
                'password': generate_password_hash(password)
            }
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/home')
def home():
    if not is_logged_in():
        flash('Please log in to continue!', 'warning')
        return redirect(url_for('login'))
    return render_template('home.html', username=session.get('username', 'User'))

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if not is_logged_in():
        flash('Please log in to continue!', 'warning')
        return redirect(url_for('login'))

    prediction_result = None

    if request.method == 'POST':
        try:
            pregnancies = int(request.form.get('pregnancies', 0))
            glucose = float(request.form.get('glucose', 0))
            blood_pressure = float(request.form.get('blood_pressure', 0))
            skin_thickness = float(request.form.get('skin_thickness', 0))
            insulin = float(request.form.get('insulin', 0))
            bmi = float(request.form.get('bmi', 0))
            diabetes_pedigree = float(request.form.get('diabetes_pedigree', 0))
            age = int(request.form.get('age', 0))

            input_data = [pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, diabetes_pedigree, age]
            prediction_result = predict_diabetes(input_data, model)

            # Save to DB
            conn = sqlite3.connect('app.db')
            c = conn.cursor()
            c.execute('''
                INSERT INTO predictions (email, pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, diabetes_pedigree, age, result)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (session['user_id'], pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, diabetes_pedigree, age, prediction_result))
            conn.commit()
            conn.close()

            session['prediction'] = prediction_result
            return redirect(url_for('advice'))

        except ValueError as e:
            flash(f'Invalid input: {str(e)}', 'danger')

    return render_template('predict.html')

@app.route('/advice')
def advice():
    if not is_logged_in():
        flash('Please log in to continue!', 'warning')
        return redirect(url_for('login'))

    prediction = session.get('prediction')
    if prediction is None:
        flash('No prediction found. Please submit the form first.', 'warning')
        return redirect(url_for('predict'))

    return render_template('advice.html', prediction=prediction)

@app.route('/history')
def history():
    if not is_logged_in():
        flash('Please log in to continue!', 'warning')
        return redirect(url_for('login'))

    conn = sqlite3.connect('app.db')
    c = conn.cursor()
    c.execute('SELECT * FROM predictions WHERE email = ?', (session['user_id'],))
    predictions = c.fetchall()
    conn.close()

    return render_template('history.html', predictions=predictions)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
