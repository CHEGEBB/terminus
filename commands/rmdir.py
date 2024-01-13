import os
import pyttsx3
import speech_recognition as sr

def execute_command(args):
    try:
        # Extracting the directory name from the command
        directory_name = ' '.join(args[2:])
        
        # Initializing pyttsx3
        engine = pyttsx3.init()
        
        # Initializing speech recognition
        r = sr.Recognizer()

        # Asking the user for the directory name
        engine.say("To remove a directory, please tell me the name of the directory.")
        engine.runAndWait()

        # Listening for the directory name
        with sr.Microphone() as source:
            print("Listening for directory name...")
            r.pause_threshold = 1
            audio = r.listen(source)
            print("Recognizing...")
            directory_name = r.recognize_google(audio, language='en-in').lower()
            print(directory_name)
        
        # Removing the directory
        os.rmdir(directory_name)
        
        # Informing the user about the result
        if not os.path.exists(directory_name):
            print(f"Directory '{directory_name}' removed successfully.")
            engine.say(f"Directory '{directory_name}' removed successfully.")
        else:
            print(f"Error: Directory '{directory_name}' removal unsuccessful.")
            engine.say(f"Error: Directory '{directory_name}' removal unsuccessful.")
        
        engine.runAndWait()
    except Exception as e:
        print(f"Error: {e}")
        engine.say(f"Error: {e}")
        engine.runAndWait()

if __name__ == "__main__":
    execute_command(['rmdir', 'remove', 'a', 'directory'])
