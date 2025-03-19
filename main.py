import os
import sys
import datetime
import time
import pygame
import webbrowser
import threading
from flask import Flask, render_template, request, redirect, url_for, session
from data_manager import DataManager

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'))


# Check and install dependencies (for Kali Linux)
def install_dependencies():
    try:
        import pkg_resources
        required = {'flask', 'pygame'}  # Need Flask and pygame now
        installed = {pkg.key for pkg in pkg_resources.working_set}
        missing = required - installed
        if missing:
            print("Installing missing dependencies...")
            os.system('pip install ' + ' '.join(missing))
    except Exception as e:
        print(f"Dependency error: {e}")

install_dependencies()

app = Flask(__name__)
app.secret_key = 'super_secret_key'  # Needed for session management

class GlobalStudentEventGuide:
    def __init__(self):
        self.data = DataManager()
        self.greetings = {
            'sports': "Hey sports star, ",
            'tech': "Hello coder, ",
            'music': "Namaste singer, ",
            'arts': "Hey dancer, "
        }

    def suggest_events(self, student_id):
        events = self.data.suggest_events(student_id)
        hobby = self.data.students.get(student_id, {}).get('hobby', 'sports')
        greeting = self.greetings.get(hobby, "Hey, ") + events[0] + " try this!"
        return f"{greeting} More options: {', '.join(events[1:])}", events[0]

gseg = GlobalStudentEventGuide()

# Dummy user database (for login and registration)
users = {
    'student1': 'password123',
    'student2': 'pass456'
}

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="Invalid username or password!")
    return render_template('login.html', error=None)

@app.route('/register', methods=['GET', 'POST'])
def register():
    # Registration route for creating new accounts
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            error = "Passwords do not match!"
            return render_template('register.html', error=error)
        
        if username in users:
            error = "User already exists!"
            return render_template('register.html', error=error)
        
        # Add new user to the dummy database
        users[username] = password
        return redirect(url_for('login'))
    
    return render_template('register.html', error=None)

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    message = None
    events = None
    reminder = None
    vr_event = None

    if request.method == 'POST':
        action = request.form.get('action')
        student_id = request.form.get('student_id', '1')

        if action == 'save_student':
            hobby = request.form.get('hobby')
            message = gseg.data.save_student(student_id, hobby)
        elif action == 'suggest_events':
            events, vr_event = gseg.suggest_events(student_id)
        elif action == 'set_reminder':
            message_text = request.form.get('message')
            seconds = int(request.form.get('seconds'))
            message = gseg.data.set_reminder(student_id, message_text, seconds)
        elif action == 'check_reminder':
            reminder = gseg.data.check_reminder() or "No reminder now!"

    return render_template('dashboard.html', message=message, events=events, reminder=reminder, vr_event=vr_event)

@app.route('/vr/<event>')
def vr(event):
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption(f"VR View: {event}")
    font = pygame.font.Font(None, 36)
    text = font.render(f"Imagine {event}!", True, (255, 255, 255))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 0, 0))
        screen.blit(text, (300, 250))
        pygame.display.flip()
    pygame.quit()
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

# Function to automatically open the default web browser
def open_browser():
    webbrowser.open_new("http://192.168.166.234:5000")

if __name__ == '__main__':
    # Delay the browser opening to allow the server to start up
    threading.Timer(1, open_browser).start()
    app.run(debug=True, host='0.0.0.0', port=5000)
   
 ##Whats Up Teammates