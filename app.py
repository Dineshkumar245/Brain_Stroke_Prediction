from flask.helpers import url_for
import numpy as np
import pandas as pd
from flask import Flask, request, render_template, redirect, session
import pickle
from werkzeug.security import generate_password_hash, check_password_hash
from database import init_db, add_user, get_user, save_user_input

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management
model = pickle.load(open('model.pickle', 'rb'))

# Initialize the database
init_db()  

@app.route("/")
def home():
    return render_template('home.html')  # Render home page for all users

@app.route("/index")
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        add_user(username, password)
        return redirect(url_for('login'))  # Redirect to login after registration
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = get_user(username)
        if user and check_password_hash(user[2], password):  # Validate credentials
            session['username'] = username  # Store username in session
            return redirect(url_for('index'))  # Redirect to home after successful login
        else:
            return render_template('login.html', error='Invalid credentials')  # Pass error message to the template
    return render_template('login.html')  # Show login form

@app.route('/logout')
def logout():
    session.pop('username', None)  # Clear session
    return redirect(url_for('home'))  # Redirect to home page after logout

@app.route('/result', methods=['GET', 'POST'])
def predict():
    if 'username' not in session:  # Check if user is logged in
        return redirect(url_for('login'))  # Redirect to login if not

    if request.method == "POST":
        # Extract features from the form
        gender_Male = int(request.form['gender'])
        age = int(request.form['age'])
        hypertension_1 = int(request.form['hypertension'])
        heart_disease_1 = int(request.form['disease'])
        ever_married_Yes = int(request.form['married'])
        work = int(request.form['work'])
        Residence_type_Urban = int(request.form['residence'])
        avg_glucose_level = float(request.form['avg_glucose_level'])
        bmi = float(request.form['bmi'])
        smoking = int(request.form['smoking'])

        # Work type encoding
        work_type_Never_worked = 1 if work == 1 else 0
        work_type_Private = 1 if work == 2 else 0
        work_type_Self_employed = 1 if work == 3 else 0
        work_type_children = 1 if work == 4 else 0
        
        # Smoking status encoding
        smoking_status_formerly_smoked = 1 if smoking == 1 else 0
        smoking_status_never_smoked = 1 if smoking == 2 else 0
        smoking_status_smokes = 1 if smoking == 3 else 0

        # Prepare input features for prediction
        input_features = [age, avg_glucose_level, bmi, gender_Male, hypertension_1, heart_disease_1,
                          ever_married_Yes, work_type_Never_worked, work_type_Private,
                          work_type_Self_employed, work_type_children, Residence_type_Urban,
                          smoking_status_formerly_smoked, smoking_status_never_smoked, smoking_status_smokes]

        # Create DataFrame for prediction
        df = pd.DataFrame([input_features], columns=['age', 'avg_glucose_level', 'bmi', 'gender_Male',
                                                     'hypertension_1', 'heart_disease_1', 'ever_married_Yes',
                                                     'work_type_Never_worked', 'work_type_Private',
                                                     'work_type_Self-employed', 'work_type_children',
                                                     'Residence_type_Urban', 'smoking_status_formerly smoked',
                                                     'smoking_status_never smoked', 'smoking_status_smokes'])

        # Make prediction
        prediction = model.predict(df)[0]

        # Save the user input and prediction to the database
        username = session['username']
        save_user_input(username, gender_Male, age, hypertension_1, heart_disease_1, ever_married_Yes, work,
                        Residence_type_Urban, avg_glucose_level, bmi, smoking, prediction)

        # Render prediction result
        if prediction == 1:
            return render_template('index.html', prediction_text='Patient has stroke risk')
        else:
            return render_template('index.html', prediction_text='Congratulations, patient does not have stroke risk')

if __name__ == "__main__":
    app.run(debug=True)  # Run the app in debug mode for better error messages
