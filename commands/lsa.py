import os
import pyttsx3
import speech_recognition as sr

def execute_command(args):
    try:
        # Extracting any additional arguments (e.g., filtering options) from the command
        options = ' '.join(args[1:])
        
        # Initializing pyttsx3
        engine = pyttsx3.init()
        
        # Initializing speech recognition
        r = sr.Recognizer()

        # Asking the user for any specific options
        engine.say("Please specify any options for the list command.")
        engine.runAndWait()

        # Listening for options
        with sr.Microphone() as source:
            print("Listening for options...")
            r.pause_threshold = 1
            audio = r.listen(source)
            print("Recognizing...")
            options = r.recognize_google(audio, language='en-in').lower()
            print(options)

        # Getting the list of files and directories
        files_and_directories = os.listdir()

        # Filtering based on any provided options
        if options:
            files_and_directories = [item for item in files_and_directories if options.lower() in item.lower()]
        
        # Informing the user about the result
        if files_and_directories:
            print(f"List of files and directories: {files_and_directories}")
            engine.say(f"List of files and directories: {files_and_directories}")
        else:
            print("No files or directories found.")
            engine.say("No files or directories found.")
        
        engine.runAndWait()
    except Exception as e:
        print(f"Error: {e}")
        engine.say(f"Error: {e}")
        engine.runAndWait()

if __name__ == "__main__":
    # Uncomment the next line if you want to test the script independently
    execute_command(['lsa'])
