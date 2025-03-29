import datetime
import time
import json
import os

class DataManager:
    def __init__(self, filename="data.json"):
        self.filename = filename
        self.students = {}
        self.events = {
            'sports': ['Arm Wrestling', 'Cricket Match'],
            'tech': ['Coding Contest'],
            'music': ['Singing Show'],
            'arts': ['Dance Competition']
        }
        self.reminders = []
        self.load_data()  # Load data from file when initializing

    def load_data(self):
        """Load students and reminders from the JSON file if it exists."""
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                data = json.load(f)
                # Convert time strings back to datetime objects for students
                self.students = {
                    sid: {
                        'hobby': info['hobby'],
                        'time': datetime.datetime.fromisoformat(info['time'])
                    } for sid, info in data.get('students', {}).items()
                }
                self.reminders = data.get('reminders', [])
        else:
            # If file doesn't exist, start with empty data
            self.students = {}
            self.reminders = []

    def save_data(self):
        """Save students and reminders to the JSON file."""
        # Convert datetime objects to strings for JSON serialization
        students_serializable = {
            sid: {
                'hobby': info['hobby'],
                'time': info['time'].isoformat()
            } for sid, info in self.students.items()
        }
        data = {
            'students': students_serializable,
            'reminders': self.reminders
        }
        with open(self.filename, 'w') as f:
            json.dump(data, f, indent=2)

    def save_student(self, student_id, hobby):
        self.students[student_id] = {'hobby': hobby.lower(), 'time': datetime.datetime.now()}
        self.save_data()  # Save to file after updating
        return f"Student {student_id} saved with hobby {hobby}!"

    def suggest_events(self, student_id):
        hobby = self.students.get(student_id, {}).get('hobby', 'sports')
        if hobby in self.events:
            return self.events[hobby]
        return self.events['sports']

    def set_reminder(self, student_id, message, seconds):
        self.reminders.append({'id': student_id, 'msg': message, 'time': time.time() + seconds})
        self.save_data()  # Save to file after updating
        return f"Reminder set for {student_id}: {message} in {seconds} seconds"

    def check_reminder(self):
        now = time.time()
        for reminder in self.reminders[:]:
            if now >= reminder['time']:
                self.reminders.remove(reminder)
                self.save_data()  # Save to file after removing
                return f"Reminder for {reminder['id']}: {reminder['msg']}"
        return None

def main():
    dm = DataManager()
    # Test the functionality
    print(">>> dm.save_student('123', 'tech')")
    print(dm.save_student('123', 'tech'))
    print(">>> dm.set_reminder('123', 'Start coding', 5)")
    print(dm.set_reminder('123', 'Start coding', 5))
    # Simulate checking reminders
    print("Checking reminders...")
    for _ in range(10):  # Check for 10 seconds
        reminder = dm.check_reminder()
        if reminder:
            print(reminder)
        time.sleep(1)

if __name__ == "__main__":
    main()