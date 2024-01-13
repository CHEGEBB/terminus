import os
import shutil
import pyttsx3
import speech_recognition as sr

def execute_command(args):
    try:
        # Extracting the source and destination directory names from the command
        source_directory = ' '.join(args[1:3])
        destination_directory = ' '.join(args[3:])
        
        # Initializing pyttsx3
        engine = pyttsx3.init()
        
        # Initializing speech recognition
        r = sr.Recognizer()

        # Asking the user for the source directory name
        engine.say("To move or rename a directory, please tell me the current name or path of the directory.")
        engine.runAndWait()

        # Listening for the source directory name
        with sr.Microphone() as source:
            print("Listening for source directory name...")
            r.pause_threshold = 1
            audio = r.listen(source)
            print("Recognizing...")
            source_directory = r.recognize_google(audio, language='en-in').lower()
            print(source_directory)

        # Asking the user for the destination directory name
        engine.say("Now, please tell me the new name or path for the directory.")
        engine.runAndWait()

        # Listening for the destination directory name
        with sr.Microphone() as source:
            print("Listening for destination directory name...")
            r.pause_threshold = 1
            audio = r.listen(source)
            print("Recognizing...")
            destination_directory = r.recognize_google(audio, language='en-in').lower()
            print(destination_directory)
        
        # Moving or renaming the directory
        shutil.move(source_directory, destination_directory)
        
        # Informing the user about the result
        if os.path.exists(destination_directory):
            print(f"Directory '{source_directory}' moved or renamed to '{destination_directory}' successfully.")
            engine.say(f"Directory '{source_directory}' moved or renamed to '{destination_directory}' successfully.")
        else:
            print(f"Error: Moving or renaming directory '{source_directory}' unsuccessful.")
            engine.say(f"Error: Moving or renaming directory '{source_directory}' unsuccessful.")
        
        engine.runAndWait()
    except Exception as e:
        print(f"Error: {e}")
        engine.say(f"Error: {e}")
        engine.runAndWait()

if __name__ == "__main__":
    # Uncomment the next line if you want to test the script independently
    execute_command(['mvdir', 'source_directory', 'destination_directory'])
