import wolframalpha
import wikipedia
import webbrowser
import pyttsx3
import speech_recognition as sr
from googlesearch import search
from utils.task_automation import *
import os
from dotenv import load_dotenv

class ChatBot:
    def __init__(self):
        self.client = wolframalpha.Client(os.getenv("WOLFRAM_ALPHA_API_KEY"))
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.task_automation = TaskAutomation()  # Initialize TaskAutomation object

    def speak(self, audio):
        self.engine.say(audio)
        self.engine.runAndWait()

    def take_command(self):
        with sr.Microphone() as source:
            print("Listening...")
            self.recognizer.pause_threshold = 1
            audio = self.recognizer.listen(source)

        try:
            print("Recognizing...")
            query = self.recognizer.recognize_google(audio, language='en-in')
            print(query)
            return query.lower()
        except Exception as e:
            print(e)
            self.speak("Sorry, I didn't catch that. Can you please repeat?")
            return "None"

    def wolfram_alpha_query(self, query):
        try:
            res = self.client.query(query)
            answer = next(res.results).text
            self.speak(answer)
        except Exception as e:
            print(e)
            self.speak("Sorry, I couldn't find an answer for that.")

    def main_loop(self):
        self.speak("Hello! I am your chatbot. How can I assist you today?")
        
        while True:
            query = self.take_command().lower()

            if 'search' in query:
                self.speak("What do you want to search for?")
                search_query = self.take_command().lower()
                for url in search(search_query, tld='com.pk', lang='es', stop=5):
                    webbrowser.open(url)
                    break
            elif 'open website' in query:
                self.speak("Sure, which website would you like to open?")
                website = self.take_command().lower()
                webbrowser.open(website)
            elif 'time' in query:
                # Code to get the current time
                pass
            elif 'calculate' in query:
                self.speak("What would you like to calculate?")
                calc_query = self.take_command().lower()
                self.wolfram_alpha_query(calc_query)
            elif 'tell me about' in query:
                self.speak("Sure, let me find information about that.")
                topic = query.replace("tell me about", "").strip()
                try:
                    result = wikipedia.summary(topic, sentences=2)
                    print(result)
                    self.speak(result)
                except wikipedia.exceptions.DisambiguationError as de:
                    self.speak(f"There are many things related to {topic}. Kindly specify which one.")
                except wikipedia.exceptions.PageError as pe:
                    self.speak(f"Sorry, I couldn't find information about {topic} on Wikipedia.")
            elif 'perform task automation' in query:
                self.task_automation.perform_task_automation()  # Call the method from the TaskAutomation class
            elif 'exit' in query:
                self.speak("Thank you. Have a great day!")
                break
            else:
                self.speak("I'm here to help. Please ask me something or give me a command.")

if __name__ == "__main__":
    chatbot = ChatBot()
    chatbot.main_loop()
