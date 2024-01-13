import os
import pyttsx3
import speech_recognition as sr

def execute_command(args):
    try:
        # Extracting the file name and program to open with from the command
        file_name = args[1]
        program_name = ' '.join(args[3:])
        
        # Initializing pyttsx3
        engine = pyttsx3.init()
        
        # Initializing speech recognition
        r = sr.Recognizer()

        # Asking the user for the program to open the file with
        engine.say("To open a file with a specific program, please tell me the name of the program.")
        engine.runAndWait()

        # Listening for the program name
        with sr.Microphone() as source:
            print("Listening for program name...")
            r.pause_threshold = 1
            audio = r.listen(source)
            print("Recognizing...")
            program_name = r.recognize_google(audio, language='en-in').lower()
            print(program_name)

        # Opening the file with the specified program
        os.system(f"{program_name} {file_name}")
        
        print(f"File '{file_name}' opened with '{program_name}' successfully.")
        engine.say(f"File '{file_name}' opened with '{program_name}' successfully.")
        engine.runAndWait()

    except Exception as e:
        print(f"Error: {e}")
        engine.say(f"Error: {e}")
        engine.runAndWait()

if __name__ == "__main__":
    # Uncomment the next line if you want to test the script independently
    execute_command(['openwith', 'file.txt', 'with', 'program'])
