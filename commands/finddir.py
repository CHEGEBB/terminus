import os
import pyttsx3
import speech_recognition as sr

def execute_command(args):
    try:
        # Extracting the directory name to find from the command
        directory_name = ' '.join(args[1:])
        
        # Initializing pyttsx3
        engine = pyttsx3.init()
        
        # Initializing speech recognition
        r = sr.Recognizer()

        # Asking the user for the directory name to find
        engine.say("To find a directory, please tell me the name of the directory.")
        engine.runAndWait()

        # Listening for the directory name
        with sr.Microphone() as source:
            print("Listening for directory name to find...")
            r.pause_threshold = 1
            audio = r.listen(source)
            print("Recognizing...")
            directory_name = r.recognize_google(audio, language='en-in').lower()
            print(directory_name)
        
        # Searching for the directory
        matching_directories = [dir for dir in os.listdir() if directory_name in dir.lower()]

        # Informing the user about the result
        if matching_directories:
            print(f"Found directories matching '{directory_name}': {matching_directories}")
            engine.say(f"Found directories matching '{directory_name}': {matching_directories}")
        else:
            print(f"No directories found matching '{directory_name}'.")
            engine.say(f"No directories found matching '{directory_name}'.")
        
        engine.runAndWait()
    except Exception as e:
        print(f"Error: {e}")
        engine.say(f"Error: {e}")
        engine.runAndWait()

if __name__ == "__main__":
    # Uncomment the next line if you want to test the script independently
    execute_command(['finddir', 'search', 'directory'])
