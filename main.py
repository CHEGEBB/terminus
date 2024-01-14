# main.py

import os
import json
import webbrowser
import sys
import speech_recognition as sr
import pyttsx3
from commands import mkdir, rmdir, mkfile, rmfile, cd, ls, lsa, lsl, lsla, cpfile, mvfile, cpdir, mvdir, rnfile, rndir, openfile, opendir, openwith, findfile, finddir
from utils import system_info, web_search, automation, reminders,  text_to_speech, translation, weather, file_operations, chatbot, media_control, task_automation, learning

# Initializing pyttsx3 and speech recognition
engine = pyttsx3.init()
recognizer = sr.Recognizer()

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def take_command():
    try:
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.pause_threshold = 1
            audio = recognizer.listen(source)
            print("Recognizing...")
            query = recognizer.recognize_google(audio, language='en-in')
            print(query)
    except Exception as e:
        print(e)
        print("Say that again please...")
        return "None"
    return query.lower()

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
    path = 'commands'  # Adjust the path based on your actual directory structure
    os.chdir(path)
    
    # List available commands
    speak("Available commands are:")
    for cmd_file in os.listdir():
        if cmd_file.endswith(".py") and cmd_file != "__init__.py":
            speak(cmd_file[:-3])
    
    speak("Please tell me which command you want to run")
    query = take_command().lower()  # Convert the query to lowercase

    # Execute the selected command
    execute_command(query.split()[0], query.split())

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

def execute_system_info():
    sys_info = system_info.SystemInfo()
    sys_info.display_system_info()

def execute_chatbot():
    chat_bot = chatbot.ChatBot()  # Corrected class name
    chat_bot.main_loop()

def execute_web_search(query):
    speak("Where would you like me to search? Wikipedia or Google?")
    choice = take_command().lower()

    if 'wikipedia' in choice:
        web_search.search_wikipedia(query)
    elif 'google' in choice:
        web_search.search_google(query)
    else:
        speak("Invalid choice. Please say 'Wikipedia' or 'Google'.")
def execute_weather():
    speak("Fetching weather information...")
    os.system('python3 commands/weather.py')  # Run weather.py as a separate process
    command_executed()

def execute_translation():
    translation.main()

if __name__ == "__main__":
    speak("Hello! I am Terminus, your terminal voice assistant.")
    speak("How may I assist you?")
    
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
        elif 'display system information' in query or 'system info' in query:
            execute_system_info()
            command_executed()
        elif 'open chatbot' in query:
            execute_chatbot()
            command_executed()
        elif 'search' in query or 'what is' in query or 'tell me about' in query:
            speak("What do you want to search for?")
            search_query = take_command().lower()
            execute_web_search(search_query)
            command_executed()
        elif 'weather' in query or 'forecast' in query:
             weather.main()  # Call the main function from weather.py
             command_executed()

        elif 'translate' in query:
            execute_translation()
            command_executed()
        elif 'exit' in query:
            speak("Thank You")
            sys.exit()
        else:
            command_not_found()
            speak("What else can I help you with?")
