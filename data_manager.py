import datetime
import time

class DataManager:
    def __init__(self):
        self.students = {}  # Store student details here
        self.events = {  # Simple list of events
            'sports': ['Arm Wrestling', 'Cricket Match'],
            'tech': ['Coding Contest'],
            'music': ['Singing Show'],
            'arts': ['Dance Competition']
        }
        self.reminders = []

    def save_student(self, student_id, hobby):
        self.students[student_id] = {'hobby': hobby.lower(), 'time': datetime.datetime.now()}
        return f"Student {student_id} saved with hobby {hobby}!"

    def suggest_events(self, student_id):
        hobby = self.students.get(student_id, {}).get('hobby', 'sports')
        if hobby in self.events:
            return self.events[hobby]
        return self.events['sports']  # Default to sports if no match

    def set_reminder(self, student_id, message, seconds):
        self.reminders.append({'id': student_id, 'msg': message, 'time': time.time() + seconds})
        return f"Reminder set for {student_id}: {message} in {seconds} seconds"

    def check_reminder(self):
        now = time.time()
        for reminder in self.reminders[:]:
            if now >= reminder['time']:
                self.reminders.remove(reminder)
                return f"Reminder for {reminder['id']}: {reminder['msg']}"
        return None
    