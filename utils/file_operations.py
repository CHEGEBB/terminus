# file_operations.py

import os
import speech_recognition as sr
from utils import text_to_speech

recognizer = sr.Recognizer()

def take_voice_command():
    with sr.Microphone() as source:
        print("Listening for file operations command...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

        try:
            print("Recognizing...")
            command = recognizer.recognize_google(audio).lower()
            print(f"User command: {command}")
            return command
        except sr.UnknownValueError:
            print("Could not understand audio.")
            return None
        except sr.RequestError as e:
            print(f"Error connecting to Google API: {e}")
            return None

def perform_file_operation(command):
    # Define your file operation logic based on the recognized command
    if 'list files' in command:
        list_files()
    elif 'create directory' in command:
        create_directory()
    elif 'delete directory' in command:
        delete_directory()
    # Add more file operations as needed

def list_files():
    files = os.listdir()
    if files:
        print("Files in the current directory:")
        for file in files:
            print(file)
        text_to_speech.speak("Listing files in the current directory.")
    else:
        print("No files found.")
        text_to_speech.speak("No files found in the current directory.")

def create_directory():
    text_to_speech.speak("Please tell me the name of the directory you want to create.")
    directory_name = take_voice_command()

    if directory_name:
        try:
            os.mkdir(directory_name)
            print(f"Directory '{directory_name}' created.")
            text_to_speech.speak(f"Directory '{directory_name}' created successfully.")
        except FileExistsError:
            print(f"Directory '{directory_name}' already exists.")
            text_to_speech.speak(f"Directory '{directory_name}' already exists.")

def delete_directory():
    text_to_speech.speak("Please tell me the name of the directory you want to delete.")
    directory_name = take_voice_command()

    if directory_name:
        try:
            os.rmdir(directory_name)
            print(f"Directory '{directory_name}' deleted.")
            text_to_speech.speak(f"Directory '{directory_name}' deleted successfully.")
        except FileNotFoundError:
            print(f"Directory '{directory_name}' not found.")
            text_to_speech.speak(f"Directory '{directory_name}' not found.")
        except OSError:
            print(f"Directory '{directory_name}' is not empty. Cannot delete.")
            text_to_speech.speak(f"Directory '{directory_name}' is not empty. Cannot delete.")

if __name__ == "__main__":
    while True:
        voice_command = take_voice_command()

        if voice_command:
            if 'file operations' in voice_command:
                file_operation_command = take_voice_command()
                perform_file_operation(file_operation_command)
            elif 'exit' in voice_command:
                text_to_speech.speak("Exiting file operations.")
                break
