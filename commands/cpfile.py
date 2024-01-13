import os
import shutil
import pyttsx3
import speech_recognition as sr

def execute_command(args):
    try:
        # Extracting the source and destination file names from the command
        source_file = ' '.join(args[2:4])
        destination_file = ' '.join(args[4:])
        
        # Initializing pyttsx3
        engine = pyttsx3.init()
        
        # Initializing speech recognition
        r = sr.Recognizer()

        # Asking the user for the source file name
        engine.say("To copy a file, please tell me the name of the source file.")
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
        engine.say("Now, please tell me the name of the destination file.")
        engine.runAndWait()

        # Listening for the destination file name
        with sr.Microphone() as source:
            print("Listening for destination file name...")
            r.pause_threshold = 1
            audio = r.listen(source)
            print("Recognizing...")
            destination_file = r.recognize_google(audio, language='en-in').lower()
            print(destination_file)
        
        # Copying the file
        shutil.copy2(source_file, destination_file)
        
        # Informing the user about the result
        if os.path.exists(destination_file):
            print(f"File '{source_file}' copied to '{destination_file}' successfully.")
            engine.say(f"File '{source_file}' copied to '{destination_file}' successfully.")
        else:
            print(f"Error: Copying file '{source_file}' to '{destination_file}' unsuccessful.")
            engine.say(f"Error: Copying file '{source_file}' to '{destination_file}' unsuccessful.")
        
        engine.runAndWait()
    except Exception as e:
        print(f"Error: {e}")
        engine.say(f"Error: {e}")
        engine.runAndWait()

if __name__ == "__main__":
    # Uncomment the next line if you want to test the script independently
    execute_command(['cpfile', 'copy', 'source_file.txt', 'destination_file.txt'])
