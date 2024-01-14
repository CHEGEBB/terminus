# utils/reminders.py

import os
import json
from datetime import datetime, timedelta
import pyttsx3
from tabulate import tabulate

REMINDERS_FILE_PATH = os.path.join(os.path.dirname(__file__), '../data/reminders.json')

def load_reminders():
    if not os.path.exists(REMINDERS_FILE_PATH):
        with open(REMINDERS_FILE_PATH, 'w') as f:
            json.dump([], f)

    with open(REMINDERS_FILE_PATH, 'r') as f:
        return json.load(f)

def save_reminders(reminders):
    with open(REMINDERS_FILE_PATH, 'w') as f:
        json.dump(reminders, f, indent=2)

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def add_reminder(description, due_date):
    reminders = load_reminders()

    new_reminder = {
        'description': description,
        'due_date': due_date.strftime('%Y-%m-%d %H:%M:%S')
    }

    reminders.append(new_reminder)
    save_reminders(reminders)

def list_reminders():
    reminders = load_reminders()

    if not reminders:
        speak("No reminders found.")
    else:
        headers = ['Index', 'Description', 'Due Date']
        data = [(i+1, reminder['description'], reminder['due_date']) for i, reminder in enumerate(reminders)]
        table = tabulate(data, headers, tablefmt="pretty")
        speak("Here are your reminders:")
        speak(table)

def delete_reminder(index):
    reminders = load_reminders()

    if 1 <= index <= len(reminders):
        deleted_reminder = reminders.pop(index - 1)
        save_reminders(reminders)
        speak(f"Deleted Reminder: {deleted_reminder['description']} - Due on {deleted_reminder['due_date']}")
    else:
        speak("Invalid reminder index.")

def check_due_reminders():
    reminders = load_reminders()
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    due_reminders = [reminder for reminder in reminders if reminder['due_date'] <= current_time]

    if due_reminders:
        headers = ['Description', 'Due Date']
        data = [(reminder['description'], reminder['due_date']) for reminder in due_reminders]
        table = tabulate(data, headers, tablefmt="pretty")
        speak("Due Reminders:")
        speak(table)
    else:
        speak("No due reminders.")

def voice_controlled_reminders():
    list_reminders()  # Display reminders first

    speak("How can I assist you with reminders?")

    try:
        command = input("You said: ").lower()

        if "add reminder" in command:
            speak("Please tell me the description of the reminder.")
            description = input("Description: ").lower()
            speak("Please tell me the due date and time of the reminder (YYYY-MM-DD HH:MM:SS).")
            due_date = input("Due Date and Time: ")
            due_date = datetime.strptime(due_date, '%Y-%m-%d %H:%M:%S')
            add_reminder(description, due_date)
            speak("Reminder added successfully.")

        elif "delete reminder" in command:
            speak("Please tell me the index of the reminder you want to delete.")
            index = int(input("Index: "))
            delete_reminder(index)

        elif "check due reminders" in command:
            check_due_reminders()

        else:
            speak("Sorry, I didn't understand the command.")

    except ValueError:
        speak("Invalid input. Please provide a valid input.")

if __name__ == "__main__":
    voice_controlled_reminders()
