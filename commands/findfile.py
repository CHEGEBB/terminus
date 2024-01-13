import os
import pyttsx3
import speech_recognition as sr

def execute_command(args):
    try:
        # Extracting the file name to find from the command
        file_name = ' '.join(args[1:])
        
        # Initializing pyttsx3
        engine = pyttsx3.init()
        
        # Initializing speech recognition
        r = sr.Recognizer()

        # Asking the user for the file name to find
        engine.say("To find a file, please tell me the name of the file.")
        engine.runAndWait()

        # Listening for the file name
        with sr.Microphone() as source:
            print("Listening for file name to find...")
            r.pause_threshold = 1
            audio = r.listen(source)
            print("Recognizing...")
            file_name = r.recognize_google(audio, language='en-in').lower()
            print(file_name)
        
        # Searching for the file
        matching_files = [file for file in os.listdir() if file_name in file.lower()]

        # Informing the user about the result
        if matching_files:
            print(f"Found files matching '{file_name}': {matching_files}")
            engine.say(f"Found files matching '{file_name}': {matching_files}")
        else:
            print(f"No files found matching '{file_name}'.")
            engine.say(f"No files found matching '{file_name}'.")
        
        engine.runAndWait()
    except Exception as e:
        print(f"Error: {e}")
        engine.say(f"Error: {e}")
        engine.runAndWait()

if __name__ == "__main__":
    # Uncomment the next line if you want to test the script independently
    execute_command(['findfile', 'search', 'file'])
