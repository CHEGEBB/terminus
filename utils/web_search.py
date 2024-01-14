# utils/web_search.py

import speech_recognition as sr
import pyttsx3
import webbrowser
import sys
import wikipedia
from googlesearch import search

def speak(audio):
    engine = pyttsx3.init()
    engine.say(audio)
    engine.runAndWait()

def show_commands():
    speak("You can ask me to search for something, or tell me about a specific topic.")
    speak("For example, you can say 'Search for Python programming' or 'Tell me about Albert Einstein'.")
    speak("If you want to exit, just say 'Exit'.")
    speak("How can I assist you?")

def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language='en-in')
        print(query)
        return query.lower()
    except Exception as e:
        print(e)
        speak("Sorry, I didn't catch that. Can you please repeat?")
        return "None"

def search_wikipedia(query):
    try:
        result = wikipedia.summary(query, sentences=2)
        print(result)
        speak(result)
        speak("If you want more information, I can search on Google as well. Do you want me to search on Google?")
        choice = take_command().lower()
        print(f"User's choice: {choice}")
        if 'yes' in choice or 'ok' in choice or 'sure' in choice:
            speak("Great! Allow me to open the web browser for you.")
            for url in search(query, tld='com.pk', lang='es', stop=5):
                webbrowser.open(url)
                break
        else:
            speak("Ok! No problem.")
    except wikipedia.exceptions.DisambiguationError as de:
        speak(f"There are many things related to {query}. Kindly specify which {query}.")
    except wikipedia.exceptions.PageError as pe:
        speak(f"Sorry, I couldn't find information about {query} on Wikipedia.")

if __name__ == "__main__":
    show_commands()

    while True:
        query = take_command().lower()

        if 'search' in query or 'tell me about' in query:
            speak("What do you want to search for?")
            search_query = take_command().lower()
            search_wikipedia(search_query)

        elif 'exit' in query:
            speak("Thank you. Have a great day!")
            sys.exit()
