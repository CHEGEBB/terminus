import os
import shutil
import pyttsx3
import speech_recognition as sr

def execute_command(args):
    try:
        # Extracting the source and destination file names from the command
        source_file = ' '.join(args[1:3])
        destination_file = ' '.join(args[3:])
        
        # Initializing pyttsx3
        engine = pyttsx3.init()
        
        # Initializing speech recognition
        r = sr.Recognizer()

        # Asking the user for the source file name
        engine.say("To move or rename a file, please tell me the current name or path of the file.")
        engine.runAndWait()

        # Listening for the source file name
        with sr.Microphone() as source:
            print("Listening for source file name...")
            r.pause_threshold = 1
            audio = r.listen(source)
            print("Recognizing...")
            source_file = r.recognize_google(audio, language='en-in').lower()
            print(source_file)

        # Asking the user for the destination file name
        engine.say("Now, please tell me the new name or path for the file.")
        engine.runAndWait()

        # Listening for the destination file name
        with sr.Microphone() as source:
            print("Listening for destination file name...")
            r.pause_threshold = 1
            audio = r.listen(source)
            print("Recognizing...")
            destination_file = r.recognize_google(audio, language='en-in').lower()
            print(destination_file)
        
        # Moving or renaming the file
        shutil.move(source_file, destination_file)
        
        # Informing the user about the result
        if os.path.exists(destination_file):
            print(f"File '{source_file}' moved or renamed to '{destination_file}' successfully.")
            engine.say(f"File '{source_file}' moved or renamed to '{destination_file}' successfully.")
        else:
            print(f"Error: Moving or renaming file '{source_file}' unsuccessful.")
            engine.say(f"Error: Moving or renaming file '{source_file}' unsuccessful.")
        
        engine.runAndWait()
    except Exception as e:
        print(f"Error: {e}")
        engine.say(f"Error: {e}")
        engine.runAndWait()

if __name__ == "__main__":
    # Uncomment the next line if you want to test the script independently
    execute_command(['mvfile', 'source_file.txt', 'destination_file.txt'])
