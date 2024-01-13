import os
import json
import time
import webbrowser
import sys
import speech_recognition as sr
import pyttsx3
from commands import mkdir
from commands import rmdir
from commands import mkfile
from commands import rmfile
from commands import cd
from commands import ls
from commands import lsa
from commands import lsl
from commands import lsla
from commands import cpfile
from commands import mvfile
from commands import cpdir
from commands import mvdir
from commands import rnfile
from commands import rndir
from commands import openfile
from commands import opendir
from commands import openwith
from commands import findfile
from commands import finddir

# Initializing pyttsx3
engine = pyttsx3.init()
# Initializing speech recognition
r = sr.Recognizer()

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def take_command():
    try:
        with sr.Microphone() as source:
            print("Listening...")
            r.pause_threshold = 1
            audio = r.listen(source)
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(query)
    except Exception as e:
        print(e)
        print("Say that again please...")
        return "None"
    return query.lower()

def wish_me():
    speak("Hello! I am Terminus, your terminal voice assistant.")
    speak("To activate me, say 'Hello Terminus'.")
    print("To activate, say 'Hello Terminus'.")
    while True:
        query = take_command().lower()
        if 'hello terminus' in query:
            break

    speak("May I know your name?")
    user_name = take_command().capitalize()  # Assuming the user responds with their name
    speak(f"Nice to meet you, {user_name}!")

    hour = int(time.strftime("%H"))
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")

    speak(f"How may I assist you, {user_name}?")

def open_google():
    speak("Opening Google")
    webbrowser.open("https://www.google.com")

def open_youtube():
    speak("Opening Youtube")
    webbrowser.open("https://www.youtube.com")

def open_gmail():
    speak("Opening Gmail")
    webbrowser.open("https://mail.google.com")

def open_github():
    speak("Opening Github")
    webbrowser.open("https://github.com")

def open_stackoverflow():
    speak("Opening Stackoverflow")
    webbrowser.open("https://stackoverflow.com")

def open_whatsapp():
    speak("Opening Whatsapp")
    webbrowser.open("https://web.whatsapp.com")

def open_commands_folder():
    speak("Opening Commands Folder")
    path = '/ACCESSIBLE_TERMINAL/commands'
    os.chdir(path)
    
    # List available commands
    speak("Available commands are:")
    for cmd_file in os.listdir():
        if cmd_file.endswith(".py") and cmd_file != "__init__.py":
            speak(cmd_file[:-3])
    
    speak("Please tell me which command you want to run")
    query = take_command().lower()  # Convert the query to lowercase

    # Execute the selected command
    if 'make a directory' in query:
        execute_command('mkdir', query.split())
    elif 'remove a directory' in query:
        execute_command('rmdir', query.split())
    elif 'make a file' in query:
        execute_command('mkfile', query.split())
    elif 'remove a file' in query:
        execute_command('rmfile', query.split())
    elif 'change directory' in query:
        execute_command('cd', query.split())
    elif 'list files' in query:
        execute_command('ls', query.split())
    elif 'list all files' in query:
        execute_command('lsa', query.split())
    elif 'list files long' in query:
        execute_command('lsl', query.split())
    elif 'list all files long' in query:
        execute_command('lsla', query.split())
    elif 'copy a file' in query:
        execute_command('cpfile', query.split())
    elif 'move a file' in query:
        execute_command('mvfile', query.split())
    elif 'copy a directory' in query:
        execute_command('cpdir', query.split())
    elif 'move a directory' in query:
        execute_command('mvdir', query.split())
    elif 'rename a file' in query:
        execute_command('rnfile', query.split())
    elif 'rename a directory' in query:
        execute_command('rndir', query.split())
    elif 'open a file' in query:
        execute_command('openfile', query.split())
    elif 'open a directory' in query:
        execute_command('opendir', query.split())
    elif 'open with' in query:
        execute_command('openwith', query.split())
    elif 'find a file' in query:
        execute_command('findfile', query.split())
    elif 'find a directory' in query:
        execute_command('finddir', query.split())
    else:
        speak("Command not found")

def execute_command(command_name, args):
    # Execute the selected command
    script_path = os.path.join('commands', f"{command_name}.py")
    if os.path.exists(script_path):
        try:
            # Dynamically import and execute the command
            command_module = __import__(f'commands.{command_name}')
            command_module.execute_command(args)
            speak("Command executed successfully")
        except Exception as e:
            print(f"Error: {e}")
            speak("Command not executed successfully")
    else:
        speak("Command not found")

def open_terminal():
    speak("Opening Terminal")
    os.system('gnome-terminal')

def open_text_editor():
    speak("Opening Text Editor")
    os.system('gedit')

def open_file_manager():
    speak("Opening File Manager")
    os.system('nautilus')

def configure_voice_commands():
    speak("Opening Voice Commands Configuration")
    with open('/terminus/config.json') as json_file:
        data = json.load(json_file)
        for p in data['commands']:
            print('Command: ' + p['command'])
            print('Script: ' + p['script'])
            print('Description: ' + p['description'])
            print(' ')
    speak("Please tell me which command you want to configure")
    command = take_command()
    with open('/terminus/config.json') as json_file:
        data = json.load(json_file)
        for p in data['commands']:
            if command == p['command']:
                print('Command: ' + p['command'])
                print('Script: ' + p['script'])
                print('Description: ' + p['description'])
                print(' ')
                speak("Please tell me what changes you want to make in this command")
                changes = take_command()
                if changes == "change command":
                    speak("Please tell me new command")
                    new_command = take_command()
                    p['command'] = new_command
                    with open('/terminus/config.json', 'w') as outfile:
                        json.dump(data, outfile)
                    speak("Command changed successfully")
                elif changes == "change script":
                    speak("Please tell me new script")
                    new_script = take_command()
                    p['script'] = new_script
                    with open('/terminus/config.json', 'w') as outfile:
                        json.dump(data, outfile)
                    speak("Script changed successfully")
                elif changes == "change description":
                    speak("Please tell me new description")
                    new_description = take_command()
                    p['description'] = new_description
                    with open('/terminus/config.json', 'w') as outfile:
                        json.dump(data, outfile)
                    speak("Description changed successfully")
                elif changes == "change command and script":
                    speak("Please tell me new command")
                    new_command = take_command()
                    p['command'] = new_command
                    speak("Please tell me new script")
                    new_script = take_command()
                    p['script'] = new_script
                    with open('/terminus/config.json', 'w') as outfile:
                        json.dump(data, outfile)
                    speak("Command and Script changed successfully")

def command_executed():
    speak("Command Executed Successfully")

def command_not_executed():
    speak("Command Not Executed Successfully")

def command_not_found():
    speak("Command Not Found")

if __name__ == "__main__":
    wish_me()
    while True:
        query = take_command().lower()
        if 'open google' in query:
            open_google()
            command_executed()
        elif 'open youtube' in query:
            open_youtube()
            command_executed()
        elif 'open gmail' in query:
            open_gmail()
            command_executed()
        elif 'open github' in query:
            open_github()
            command_executed()
        elif 'open stackoverflow' in query:
            open_stackoverflow()
            command_executed()
        elif 'open whatsapp' in query:
            open_whatsapp()
            command_executed()
        elif 'open commands folder' in query:
            open_commands_folder()
            command_executed()
        elif 'open terminal' in query:
            open_terminal()
            command_executed()
        elif 'open text editor' in query:
            open_text_editor()
            command_executed()
        elif 'open file manager' in query:
            open_file_manager()
            command_executed()
        elif 'configure voice commands' in query:
            configure_voice_commands()
            command_executed()
        elif 'exit' in query:
            speak("Thank You")
            sys.exit()
        else:
            command_not_found()
