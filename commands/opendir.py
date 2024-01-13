import os
import pyttsx3
import speech_recognition as sr

def execute_command(args):
    try:
        # Extracting the directory name to open from the command
        directory_name = ' '.join(args[1:])
        
        # Initializing pyttsx3
        engine = pyttsx3.init()
        
        # Initializing speech recognition
        r = sr.Recognizer()

        # Asking the user for the directory name
        engine.say("To open a directory, please tell me the name of the directory.")
        engine.runAndWait()

        # Listening for the directory name
        with sr.Microphone() as source:
            print("Listening for directory name to open...")
            r.pause_threshold = 1
            audio = r.listen(source)
            print("Recognizing...")
            directory_name = r.recognize_google(audio, language='en-in').lower()
            print(directory_name)
        
        # Checking if the directory exists
        if os.path.exists(directory_name) and os.path.isdir(directory_name):
            # Opening the directory with the default file explorer
            os.system(f"xdg-open {directory_name}")
            print(f"Directory '{directory_name}' opened successfully.")
            engine.say(f"Directory '{directory_name}' opened successfully.")
        else:
            print(f"Error: Directory '{directory_name}' not found or is not a valid directory.")
            engine.say(f"Error: Directory '{directory_name}' not found or is not a valid directory.")
        
        engine.runAndWait()
    except Exception as e:
        print(f"Error: {e}")
        engine.say(f"Error: {e}")
        engine.runAndWait()

if __name__ == "__main__":
    # Uncomment the next line if you want to test the script independently
    execute_command(['opendir', 'open', 'directory'])
