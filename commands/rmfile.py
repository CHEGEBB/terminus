import os
import pyttsx3
import speech_recognition as sr

def execute_command(args):
    try:
        # Extracting the file name from the command
        file_name = ' '.join(args[2:])
        
        # Initializing pyttsx3
        engine = pyttsx3.init()
        
        # Initializing speech recognition
        r = sr.Recognizer()

        # Asking the user for the file name
        engine.say("To remove a file, please tell me the name of the file.")
        engine.runAndWait()

        # Listening for the file name
        with sr.Microphone() as source:
            print("Listening for file name...")
            r.pause_threshold = 1
            audio = r.listen(source)
            print("Recognizing...")
            file_name = r.recognize_google(audio, language='en-in').lower()
            print(file_name)
        
        # Removing the file
        os.remove(file_name)
        
        # Informing the user about the result
        if not os.path.exists(file_name):
            print(f"File '{file_name}' removed successfully.")
            engine.say(f"File '{file_name}' removed successfully.")
        else:
            print(f"Error: File '{file_name}' removal unsuccessful.")
            engine.say(f"Error: File '{file_name}' removal unsuccessful.")
        
        engine.runAndWait()
    except Exception as e:
        print(f"Error: {e}")
        engine.say(f"Error: {e}")
        engine.runAndWait()

if __name__ == "__main__":
    execute_command(['rmfile', 'remove', 'a', 'file'])
