from flask import Flask, request, render_template, redirect, url_for,flash,session
# import json
import numpy as np
import pandas as pd
import pickle
import psycopg2
from flask_mail import Mail, Message
app = Flask(__name__)
app.secret_key = 'a_random_and_complex_string_here'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'suprateeksen62@gmail.com'
app.config['MAIL_PASSWORD'] = 'pspy enhc rptk lgxy'
app.config['MAIL_DEFAULT_SENDER'] = 'suprateeksen62@gmail.com'

mail = Mail(app)   
def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="HealthPlus",
        user="postgres",
        password="root"
    )
    print("Connected")
    return conn
get_db_connection()
symptoms_dict = {'itching': 0, 'skin_rash': 1, 'nodal_skin_eruptions': 2, 'continuous_sneezing': 3, 'shivering': 4, 'chills': 5, 'joint_pain': 6, 'stomach_pain': 7, 'acidity': 8, 'ulcers_on_tongue': 9, 'muscle_wasting': 10, 'vomiting': 11, 'burning_micturition': 12, 'spotting_ urination': 13, 'fatigue': 14, 'weight_gain': 15, 'anxiety': 16, 'cold_hands_and_feets': 17, 'mood_swings': 18, 'weight_loss': 19, 'restlessness': 20, 'lethargy': 21, 'patches_in_throat': 22, 'irregular_sugar_level': 23, 'cough': 24, 'high_fever': 25, 'sunken_eyes': 26, 'breathlessness': 27, 'sweating': 28, 'dehydration': 29, 'indigestion': 30, 'headache': 31, 'yellowish_skin': 32, 'dark_urine': 33, 'nausea': 34, 'loss_of_appetite': 35, 'pain_behind_the_eyes': 36, 'back_pain': 37, 'constipation': 38, 'abdominal_pain': 39, 'diarrhoea': 40, 'mild_fever': 41, 'yellow_urine': 42, 'yellowing_of_eyes': 43, 'acute_liver_failure': 44, 'fluid_overload': 45, 'swelling_of_stomach': 46, 'swelled_lymph_nodes': 47, 'malaise': 48, 'blurred_and_distorted_vision': 49, 'phlegm': 50, 'throat_irritation': 51, 'redness_of_eyes': 52, 'sinus_pressure': 53, 'runny_nose': 54, 'congestion': 55, 'chest_pain': 56, 'weakness_in_limbs': 57, 'fast_heart_rate': 58, 'pain_during_bowel_movements': 59, 'pain_in_anal_region': 60, 'bloody_stool': 61, 'irritation_in_anus': 62, 'neck_pain': 63, 'dizziness': 64, 'cramps': 65, 'bruising': 66, 'obesity': 67, 'swollen_legs': 68, 'swollen_blood_vessels': 69, 'puffy_face_and_eyes': 70, 'enlarged_thyroid': 71, 'brittle_nails': 72, 'swollen_extremeties': 73, 'excessive_hunger': 74, 'extra_marital_contacts': 75, 'drying_and_tingling_lips': 76, 'slurred_speech': 77, 'knee_pain': 78, 'hip_joint_pain': 79, 'muscle_weakness': 80, 'stiff_neck': 81, 'swelling_joints': 82, 'movement_stiffness': 83, 'spinning_movements': 84, 'loss_of_balance': 85, 'unsteadiness': 86, 'weakness_of_one_body_side': 87, 'loss_of_smell': 88, 'bladder_discomfort': 89, 'foul_smell_of urine': 90, 'continuous_feel_of_urine': 91, 'passage_of_gases': 92, 'internal_itching': 93, 'toxic_look_(typhos)': 94, 'depression': 95, 'irritability': 96, 'muscle_pain': 97, 'altered_sensorium': 98, 'red_spots_over_body': 99, 'belly_pain': 100, 'abnormal_menstruation': 101, 'dischromic _patches': 102, 'watering_from_eyes': 103, 'increased_appetite': 104, 'polyuria': 105, 'family_history': 106, 'mucoid_sputum': 107, 'rusty_sputum': 108, 'lack_of_concentration': 109, 'visual_disturbances': 110, 'receiving_blood_transfusion': 111, 'receiving_unsterile_injections': 112, 'coma': 113, 'stomach_bleeding': 114, 'distention_of_abdomen': 115, 'history_of_alcohol_consumption': 116, 'fluid_overload.1': 117, 'blood_in_sputum': 118, 'prominent_veins_on_calf': 119, 'palpitations': 120, 'painful_walking': 121, 'pus_filled_pimples': 122, 'blackheads': 123, 'scurring': 124, 'skin_peeling': 125, 'silver_like_dusting': 126, 'small_dents_in_nails': 127, 'inflammatory_nails': 128, 'blister': 129, 'red_sore_around_nose': 130, 'yellow_crust_ooze': 131}
diseases_list = {15: 'Fungal infection', 4: 'Allergy', 16: 'GERD', 9: 'Chronic cholestasis', 14: 'Drug Reaction', 33: 'Peptic ulcer diseae', 1: 'AIDS', 12: 'Diabetes ', 17: 'Gastroenteritis', 6: 'Bronchial Asthma', 23: 'Hypertension ', 30: 'Migraine', 7: 'Cervical spondylosis', 32: 'Paralysis (brain hemorrhage)', 28: 'Jaundice', 29: 'Malaria', 8: 'Chicken pox', 11: 'Dengue', 37: 'Typhoid', 40: 'hepatitis A', 19: 'Hepatitis B', 20: 'Hepatitis C', 21: 'Hepatitis D', 22: 'Hepatitis E', 3: 'Alcoholic hepatitis', 36: 'Tuberculosis', 10: 'Common Cold', 34: 'Pneumonia', 13: 'Dimorphic hemmorhoids(piles)', 18: 'Heart attack', 39: 'Varicose veins', 26: 'Hypothyroidism', 24: 'Hyperthyroidism', 25: 'Hypoglycemia', 31: 'Osteoarthristis', 5: 'Arthritis', 0: '(vertigo) Paroymsal  Positional Vertigo', 2: 'Acne', 38: 'Urinary tract infection', 35: 'Psoriasis', 27: 'Impetigo'}
# Load datasets
def load_datasets():
    try:
        sym_des = pd.read_csv("datasets/symtoms_df.csv")
        precautions = pd.read_csv("datasets/precautions_df.csv")
        workout = pd.read_csv("datasets/workout_df.csv")
        description = pd.read_csv("datasets/description.csv")
        medications = pd.read_csv('datasets/medications.csv')
        diets = pd.read_csv("datasets/diets.csv")
    except FileNotFoundError as e:
        print(f"Error loading datasets: {e}")
        sym_des = precautions = workout = description = medications = diets = pd.DataFrame()
    return sym_des, precautions, workout, description, medications, diets

sym_des, precautions, workout, description, medications, diets = load_datasets()


def load_model():
    try:
        model = pickle.load(open('models/svc.pkl', 'rb'))#Pickle is used for serializing and deserializing object
    except FileNotFoundError as e:
        print(f"Error loading model: {e}")
        model = None
    return model

svc = load_model()

def helper(dis):
    if not description.empty:
        desc = description[description['Disease'] == dis]['Description']
        desc = " ".join([w for w in desc])
    else:
        desc = "Description not available"

    if not precautions.empty:
        pre = precautions[precautions['Disease'] == dis][['Precaution_1', 'Precaution_2', 'Precaution_3', 'Precaution_4']]
        pre = [col for col in pre.values]
    else:
        pre = ["Precautions not available"]

    if not medications.empty:
        med = medications[medications['Disease'] == dis]['Medication']
        med = [col for col in med.values]
        med = eval(med[0])
    else:
        med = ["Medications not available"]

    if not diets.empty:
        die = diets[diets['Disease'] == dis]['Diet']
        die = [die for die in die.values]
        die=eval(die[0])
    else:
        die = ["Diets not available"]

    if not workout.empty:
        wrkout = workout[workout['disease'] == dis]['workout']
    else:
        wrkout = ["Workouts not available"]

    return desc, pre, med, die, wrkout

def get_predicted_value(patient_symptoms):
    input_vector = np.zeros(len(symptoms_dict))
    for item in patient_symptoms:
        input_vector[symptoms_dict.get(item, -1)] = 1
    if svc:
        prediction = svc.predict([input_vector])[0]
        return diseases_list.get(prediction, "Disease not found")
    return "Model not loaded"

@app.route("/")
def index():
    return render_template("home.html")
@app.route('/index')
def i():
    return render_template('contact.html')
@app.route('/HealthCare')
def healthCare():
    return render_template('index.html')
@app.route('/logout')
def logout():
    session.clear()  # Clears all session data
    return redirect(url_for('index'))
@app.route('/sendMail')
def sendMail():
    email = session.get('user', {}).get('email', '')
    if not email:
        flash("No user is logged in.")
        return redirect(url_for('index'))
    msg = Message(subject="Your Online Disease Analysis",
                  sender='ashishmohapatrapopun@gmail.com',
                  recipients=[email])
    
    email_content=session['disease']['email']
    msg.html = email_content
    mail.send(msg)
    msg="Disease analysis report has been sent to your mail Successfully"
    return render_template('index.html',msggg=msg)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        cur = conn.cursor()
        
       
        cur.execute("SELECT * FROM patient WHERE email = %s", (username,))
        user = cur.fetchone()  
        print(user)
        
        if user:
           
            db_password = user[1]
            if password == db_password:  
                print(user)
                session['user']={
                    'username':user[2],
                    'email':user[0]
                }
                return redirect(url_for('home'))
            else:
                
                flash("Invalid password. Please try again.")
        else:
            flash("Username not found. Please try again.")
       
        
       
        cur.close()
        conn.close()
    
    return render_template('patient_login.html')

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        fullname = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        email = request.form['email']
        password = request.form['password']
        conn = get_db_connection()
        cursor = conn.cursor()

        # Insert query (ensure to hash passwords in real applications)
        insert_query = """
        INSERT INTO patient (name, age, gender, email, password)
        VALUES (%s, %s, %s, %s, %s);
        """
        cursor.execute(insert_query, (fullname, age, gender, email, password))
        
        # Commit and close the connection
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('login'))

    return render_template('register.html')
@app.route('/dregister', methods=['GET', 'POST'])
def dregister():
    if request.method == 'POST':
        # Adding the 'Dr.' prefix to the name
        name = "Dr." + " " + request.form['name']
        email = request.form['email']
        password = request.form['password']
        specialization = request.form['specialization']
        qualification = request.form['qualification']
        years_of_experience = request.form['yearsOfExperience']
        working_at = request.form['workingAt']
        consultation_hours = request.form['consultationHours']

        # Assuming profile_pic is optional
       

        # Database insertion
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Insert query (hash password before storing in real applications)
        insert_query = """
        INSERT INTO doctor (name, email, specialization, qualification, exp, workingat, consultationhours, password)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """
        
        # Executing the query with provided data
        cursor.execute(insert_query, (name, email, specialization, qualification, years_of_experience, working_at, consultation_hours, password))
        
        # Commit and close the connection
        conn.commit()
        cursor.close()
        conn.close()
        
        flash('Registration successful!', 'success')  # Flash success message
        return redirect(url_for('dlogin'))  # Redirect to the login route after successful registration

    return render_template('d_register.html')  # Render the registration page for GET request
@app.route('/dLogin', methods=['GET', 'POST'])
def dlogin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Fetch the doctor record by email
        cur.execute("SELECT * FROM doctor WHERE email = %s", (username,))
        doctor = cur.fetchone()
        print(doctor)
        
        if doctor:
            db_password = doctor[7]  # Adjust index if password is stored in a different column
            
            if password == db_password:  
                # Setting session with doctor's details
                session['doctor'] = {
                    'name': doctor[1],  # Adjust index as per your table structure
                    'email': doctor[0]
                }
                return redirect(url_for('doctorDashboard'))  # Redirect to home page or doctor dashboard
            else:
                flash("Invalid password. Please try again.")
        else:
            flash("Username not found. Please try again.")
        
        cur.close()
        conn.close()
    
    return render_template('doctor_login.html')


def convert_text_to_format(text):
    # Replace spaces with underscores only between words, while keeping commas intact
    l=text.split(',')
    l=[i.lower() for i in l]
    l=','.join(l)
    return l.replace(' ', '_')
@app.route('/predict', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        symptoms = request.form.get('symptoms')
        if not symptoms:
            message = "Please provide symptoms."
            return render_template('index.html', message=message)
        
        symptoms = convert_text_to_format(symptoms)
        email=''
        if 'user' in session:
            email=session['user']['email']
            print(email)

        user_symptoms = [s.strip() for s in symptoms.split(',')]
        user_symptoms = [symptom.strip("[]' ") for symptom in user_symptoms]
        predicted_disease = get_predicted_value(user_symptoms)
        dis_des, precautions, medications, rec_diet, workout = helper(predicted_disease)

        my_precautions = [i for i in precautions[0]]
        
        # msg = Message(subject="Your Online Disease Analysis",
        #           sender='ashishmohapatrapopun@gmail.com',
        #           recipients=[email])
        email_content = f"""
        <html lang="en">
        <!DOCTYPE html>
        <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Your Online Disease Analysis</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 20px;
                background-color: #f4f4f4;
            }}
            h1, h2, h3 {{
                color: #333;
            }}
            .container {{
                max-width: 800px;
                margin: 0 auto;
                background: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            }}
            .section {{
                margin-bottom: 20px;
            }}
            ul {{
                list-style-type: disc;
                padding-left: 20px;
            }}
        </style>
        </head>
        <body>

        <div class="container">
            <h1>Your Online Disease Analysis</h1>

            <div class="section">
                <h2>Predicted Disease</h2>
                <p><strong>{predicted_disease}</strong></p>
            </div>

            <div class="section">
                <h2>Description</h2>
                <p>{dis_des}</p>
            </div>

            <div class="section">
                <h2>Precautions</h2>
                <ul>
                    {''.join([f'<li>{my_precautions}</li>' for my_precautions in my_precautions])}
                </ul>
            </div>

            <div class="section">
                <h2>Medications</h2>
                <ul>
                    {''.join([f'<li>{med}</li>' for med in medications])}
                </ul>
            </div>

            <div class="section">
                <h2>Workouts</h2>
                <ul>
                    {''.join([f'<li>{wrk}</li>' for wrk in workout])}
                </ul>
            </div>

            <div class="section">
                <h2>Diets</h2>
                <ul>
                    {''.join([f'<li>{diet}</li>' for diet in rec_diet])}
                </ul>
            </div>
        </div>

        </body>
        </html>
        """
        session['disease']={'email':email_content}
        # msg.html = email_content
        # mail.send(msg)
       
        

        return render_template('index.html', predicted_disease=predicted_disease, dis_des=dis_des,
                               my_precautions=my_precautions, medications=medications, my_diet=rec_diet,
                               workout=workout)
    

    return render_template('index.html')

# Error handling routes
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html'), 500

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/developer')
def developer():
    return render_template("developer.html")

@app.route('/blog')
def blog():
    return render_template("blog.html")
# doctor Routes
@app.route('/doctorDashboard')
def doctorDashboard():
    conn = get_db_connection()
    cur = conn.cursor()
    name = session['doctor']
    cur.execute("SELECT count(*) FROM doctor WHERE email = %s", (name['email'],))
    count = cur.fetchone()[0]
    return render_template("doctor_dashboard.html",name=name,count=count)
@app.route('/bookAppointment')
def bookAppointment():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM doctor")
        data = cur.fetchall()
        print(data)
        return render_template('appointment.html', data=data)
    except Exception as e:
        print(f"Error: {e}")
        flash('An error occurred while fetching doctor data.', 'danger')
        return redirect(url_for('home'))  # Redirect to the homepage or another error page
    finally:
        cur.close()  # Close cursor
        conn.close()  # Close connection
@app.route('/appointment_form')
def appointment_form():
    doctor_email = request.args.get('email')  # Get doctor's email from query parameters
    try:
        # Connect to the database
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Fetch doctor data based on email
        cur.execute("SELECT * FROM doctor WHERE email = %s", (doctor_email,))
        doctor_data = cur.fetchone()
        print(doctor_data)
        print(session['user'])
        
        if doctor_data is None:
            flash('Doctor not found.', 'danger')
            return redirect(url_for('home'))  # Redirect to the homepage or another error page
        
        # Assuming you want to render the template with the doctor email and username from the session
        return render_template('appointment_form.html', doctor_email=doctor_email, doctor_data=doctor_data, user=session['user'])
    
    except Exception as e:
        # Handle the exception
        print(f"Error: {e}")
        flash('An error occurred while fetching doctor data.', 'danger')
        return redirect(url_for('home'))  # Redirect to the homepage or another error page
    
    finally:
        # Close cursor and connection
        cur.close()
        conn.close()
@app.route('/book_appointment', methods=['POST'])
def book_appointment():
    # Extract form data
    full_name = request.form['fullName']  # Patient's full name (from the form)
    appointment_date = request.form['appointmentDate']  # Appointment date (from the form)
    reason = request.form['reason']  # Reason for the appointment (from the form)
    email = request.form['email']  # Patient's email (from the form)
    status ="Pending" # Default status ("Pending" from the form)

    # Assuming doctor_email is passed through the URL query string
    doctor_email = request.args.get('email')  # Doctor's email from the URL parameter
    print(f"Doctor's email: {doctor_email}")

    try:
        # Database connection
        conn = get_db_connection()
        cur = conn.cursor()

        # Insert data into the appointment table
        query = """
        INSERT INTO appointment (patient_name, doctor_email, appointment_date, reason, patient_email, status)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cur.execute(query, (full_name, doctor_email, appointment_date, reason, email, status))
        
        # Commit the transaction to save the data
        conn.commit()
        
        # Success message
        flash('Appointment successfully booked!', 'success')
        return redirect(url_for('bookAppointment'))  # Redirect after successful booking
        
    except Exception as e:
        # If an error occurs
        print(f"Error occurred: {e}")
        flash('An error occurred while booking your appointment.', 'danger')
        return redirect(url_for('home'))
    
    finally:
        # Always close the cursor and connection
        cur.close()
        conn.close()
from flask import render_template, session
import psycopg2

@app.route('/showAppointment')
def showAppointment():
    try:
        # Database connection
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Define the SQL query with %s placeholder
        query = """
                SELECT * FROM appointment WHERE doctor_email=%s
            """
        
        # Execute the query with the email parameter from the session
        cur.execute(query, (session['doctor']['email'],))
        
        # Fetch all results
        appointments = cur.fetchall()
        print(appointments)
        
        # Render the results in the template
        return render_template('showAppointments.html', appointments=appointments)
    
    except Exception as e:
        print(f"Error occurred: {e}")
        return "An error occurred while fetching appointments."
    
    finally:
        # Ensure cursor and connection are closed
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()
@app.route('/myAppointments')
def myAppointments():
    try:
        # Database connection
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Define the SQL query with %s placeholder
        query = """
                SELECT * FROM appointment WHERE patient_email=%s
            """
        
        # Execute the query with the email parameter from the session
        cur.execute(query, (session['user']['email'],))
        
        # Fetch all results
        appointments = cur.fetchall()
        print(appointments)
        
        # Render the results in the template
        return render_template('myAppointments.html', appointments=appointments)
    
    except Exception as e:
        print(f"Error occurred: {e}")
        return "An error occurred while fetching appointments."
    
    finally:
        # Ensure cursor and connection are closed
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()

def sendMail(email, user_name, date, time):
    # Creating the email message
    msg = Message(subject="Your Online Disease Analysis and Appointment Details",
                  sender='ashishmohapatrapopun@gmail.com',
                  recipients=[email])
    
    # HTML content for the email
    email_content = f"""
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Your Appointment Confirmation</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f4f4f4;
            color: #333;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
            background: #ffffff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }}
        .header {{
            text-align: center;
            padding-bottom: 20px;
            border-bottom: 2px solid #007bff;
        }}
        h1 {{
            color: #007bff;
            font-weight: 600;
        }}
        .content {{
            margin-top: 20px;
            font-size: 1.1em;
        }}
        .appointment-details {{
            background-color: #e8f4ff;
            padding: 20px;
            border-radius: 6px;
            margin-top: 20px;
            border-left: 5px solid #007bff;
        }}
        .appointment-details p {{
            margin: 5px 0;
        }}
        .footer {{
            text-align: center;
            font-size: 0.9em;
            color: #666;
            margin-top: 30px;
            padding-top: 10px;
            border-top: 1px solid #e0e0e0;
        }}
        .button {{
            display: inline-block;
            background-color: #007bff;
            color: #fff;
            padding: 10px 20px;
            text-decoration: none;
            border-radius: 5px;
            margin-top: 20px;
        }}
    </style>
</head>
<body>

<div class="container">
    <div class="header">
        <h1>Your Appointment is Confirmed</h1>
    </div>

    <div class="content">
        <p>Dear {user_name},</p>
        <p>We are pleased to inform you that your appointment has been successfully accepted and scheduled. Below are the details of your appointment:</p>

        <div class="appointment-details">
            <h2>Appointment Details</h2>
            <p><strong>Date:</strong> {date}</p>
            <p><strong>Time:</strong> {time}</p>
        </div>

        <p>If you have any questions or need to reschedule, please contact us through our support page.</p>

        <a href="https://yourwebsite.com/contact" class="button">Contact Us</a>
    </div>

    <div class="footer">
        <p>This is an automated email. Please do not reply directly to this message.</p>
        <p>If you need further assistance, please visit our <a href="https://yourwebsite.com">website</a>.</p>
    </div>
</div>

</body>
</html>
"""

    # Set the email HTML content and send the email
    msg.html = email_content
    mail.send(msg)


# Route to approve the appointment
@app.route('/approve_appointment/<int:appointment_id>', methods=['POST'])
def approve_appointment(appointment_id):
    try:
        # Retrieve form data
        msg = request.form['message']
        date = request.form['appointment_date']
        time = request.form['appointment_time']
        
        # Connect to the database
        conn = get_db_connection()
        cur = conn.cursor()

        # Retrieve the patient's email based on appointment_id
        cur.execute("""
            SELECT patient_email,patient_name
            FROM appointment
            WHERE appointment_id = %s
        """, (appointment_id,))
        
        patient_email = cur.fetchone()
        patient_name = patient_email[1]

        if patient_email:
            email = patient_email[0]  # Extract email address
            sendMail(email,  patient_name, date, time)  # Send the email to the patient

            # Update the appointment status to 'Accepted'
            cur.execute("""
                UPDATE appointment
                SET status = 'Accepted', doctor_feedback = %s
                WHERE appointment_id = %s AND doctor_email = %s
                """, (msg, appointment_id, session['doctor']['email']))


            conn.commit()

    except Exception as e:
        print(f"Error occurred while accepting appointment: {e}")
        # Optional: You could log the error message or handle specific cases
    finally:
        cur.close()
        conn.close()

    return redirect(url_for('showAppointment'))
# /cancel_appointment/{{ appointment[0] }}
@app.route('/cancel_appointment/<int:appointment_id>', methods=['POST'])
def cancel_appointment(appointment_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Retrieve the patient's email based on appointment_id
        cur.execute("""
           delete
            FROM appointment
            WHERE appointment_id = %s
        """, (appointment_id,))
        
        conn.commit()

    except Exception as e:
        print(f"Error occurred while accepting appointment: {e}")
        # Optional: You could log the error message or handle specific cases
    finally:
        cur.close()
        conn.close()

    return redirect(url_for('myAppointments'))

@app.route('/reject_appointment/<int:appointment_id>', methods=['POST'])
def reject_appointment(appointment_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Update the appointment status to "Rejected"
        cur.execute("""
            UPDATE appointment
            SET status = 'Rejected'
            WHERE appointment_id = %s AND doctor_email = %s
        """, (appointment_id, session['doctor']['email']))
        
        conn.commit()
    except Exception as e:
        print(f"Error occurred while rejecting appointment: {e}")
    finally:
        cur.close()
        conn.close()

    return redirect(url_for('showAppointment'))



if __name__ == '__main__':
    app.run(debug=True)
