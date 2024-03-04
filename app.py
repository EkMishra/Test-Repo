# Import necessary libraries and frameworks
from flask import Flask, render_template, request, redirect, session
import mysql.connector

# Create a Flask app instance
app = Flask(_name_)

# Set up a database connection
mydb = mysql.connector.connect(
  host="localhost",
  user="yourusername",
  password="yourpassword",
  database="hackathon_management"
)

# Define routes for the different functionalities
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Query the database to check if the email and password match
        cursor = mydb.cursor()
        query = "SELECT * FROM users WHERE email=%s AND password=%s"
        values = (email, password)
        cursor.execute(query, values)
        user = cursor.fetchone()
        
        if user:
            session['user_id'] = user[0]
            session['user_name'] = user[1]
            return redirect('/dashboard')
        else:
            return render_template('login.html', error='Invalid email or password')
    else:
        return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    user_id = session['user_id']
    
    # Query the database to get the events that the user has registered for
    cursor = mydb.cursor()
    query = "SELECT * FROM events INNER JOIN registrations ON events.event_id=registrations.event_id WHERE registrations.user_id=%s"
    values = (user_id,)
    cursor.execute(query, values)
    events = cursor.fetchall()
    
    return render_template('dashboard.html', user_name=session['user_name'], events=events)

@app.route('/create-event', methods=['GET', 'POST'])
def create_event():
    if request.method == 'POST':
        event_name = request.form['event_name']
        event_description = request.form['event_description']
        
        # Insert the new event into the database
        cursor = mydb.cursor()
        query = "INSERT INTO events (event_name, event_description) VALUES (%s, %s)"
        values = (event_name, event_description)
        cursor.execute(query, values)
        mydb.commit()
        
        return redirect('/dashboard')
    else:
        return render_template('create-event.html')

# Run the Flask app
if _name_ == '_main_':
    app.secret_key = 'your_secret_key_here'
    app.run(debug=True)