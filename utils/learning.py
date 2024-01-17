import requests
import json
import random
import pyttsx3
import speech_recognition as sr
from tabulate import tabulate  # Import the tabulate module
import time

QUOTES_API_KEY = '5puUUckdHEGxeyzdyHuDhaP4FN0EGfR3RGC1OkwX'
NASA_API_KEY = '7k4b22cjrbbjg29R1VBDzEfebZkO2BRBim3mtUTX'
GOOGLE_BOOKS_API_KEY = 'AIzaSyDXn8j-bYJoojOqy303i4oGU_PKVTRhzzU'

# Initializing pyttsx3 and speech recognition
engine = pyttsx3.init()
recognizer = sr.Recognizer()

def speak_with_animation(text):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(0.05)  # Adjust the sleep duration to control the animation speed
    print()
    engine.say(text)
    engine.runAndWait()

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
        print("Say that again, please...")
        return "None"
    return query.lower()

def print_features():
    features_text = """
    I can assist you with the following features:
    1. Trivia Quiz
    2. Science Facts
    3. Quotes of the Day
    4. Book Recommendations
    5. Exit (To end the interaction)
    """
    speak_with_animation(features_text)

# Trivia Quiz using Open Trivia Database API
def trivia_quiz():
    api_url = "https://opentdb.com/api.php?amount=15"
    response = requests.get(api_url)
    
    if response.status_code == 200:
        trivia_data = response.json()
        if trivia_data["response_code"] == 0:
            questions = trivia_data["results"]
            speak_with_animation("Welcome to Trivia Quiz. Get ready for some questions!")
            speak_with_animation("I will read out a question, and you can answer by saying the corresponding option number.")
            display_trivia_questions(questions)
        else:
            speak_with_animation("Failed to fetch trivia questions.")
    else:
        speak_with_animation("Failed to connect to the Open Trivia Database.")

def display_trivia_questions(questions):
    score = 0
    recognizer = sr.Recognizer()

    for index, question in enumerate(questions, start=1):
        speak_with_animation(f"Question {index}: {question['question']}")
        options = question['incorrect_answers'] + [question['correct_answer']]
        random.shuffle(options)

        for i, option in enumerate(options, start=1):
            speak_with_animation(f"Option {i}: {option}")

        speak_with_animation("Your answer:")
        user_answer = take_trivia_answer(recognizer)
        correct_answer = options.index(question['correct_answer']) + 1

        if user_answer == correct_answer:
            speak_with_animation("Correct!")
            score += 1
        else:
            speak_with_animation(f"Wrong! The correct answer is {correct_answer}.")
    
    speak_with_animation(f"Quiz completed! Your score: {score}/{len(questions)}")

def take_trivia_answer(recognizer):
    while True:
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source, timeout=10)
            answer = recognizer.recognize_google(audio).lower()
            if "one" in answer:
                return 1
            elif "two" in answer:
                return 2
            elif "three" in answer:
                return 3
            elif "four" in answer:
                return 4
            else:
                speak_with_animation("Invalid response. Please try again.")
        except sr.UnknownValueError:
            speak_with_animation("Sorry, I didn't catch that. Can you please repeat?")
        except sr.RequestError:
            speak_with_animation("I'm having trouble accessing the microphone. Please check your connection.")

# Science Facts using NASA API
def science_facts():
    nasa_api_url = f"https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}"

    response = requests.get(nasa_api_url)
    if response.status_code == 200:
        nasa_data = response.json()
        speak_with_animation("Here is today's astronomy picture of the day.")
        speak_with_animation(nasa_data['explanation'])
    else:
        speak_with_animation("Failed to connect to the NASA API.")

# Quotes of the Day using They Said So Quotes API
def quotes_of_the_day():
    quotes_api_url = f"https://quotes.rest/qod?category=inspire&api_key={QUOTES_API_KEY}"

    response = requests.get(quotes_api_url)
    if response.status_code == 200:
        quotes_data = response.json()
        quote_content = quotes_data['contents']['quotes'][0]['quote']
        speak_with_animation(f"Here is the inspirational quote of the day: {quote_content}")
    else:
        speak_with_animation("Failed to connect to the They Said So Quotes API.")

# Google Books API for Book Recommendations
def book_recommendations():
    # Fetching book recommendations from Google Books API
    google_books_api_url = f"https://www.googleapis.com/books/v1/volumes?q=subject:programming&key={GOOGLE_BOOKS_API_KEY}"
    response = requests.get(google_books_api_url)

    if response.status_code == 200:
        books_data = response.json()
        books = books_data.get('items', [])

        if books:
            # Extracting relevant information for each book
            book_info = [(book['volumeInfo']['title'], ', '.join(book['volumeInfo']['authors']))
                         for book in books]

            # Printing book recommendations in tabular format
            headers = ["Title", "Authors"]
            table = tabulate(book_info, headers, tablefmt="grid")
            speak_with_animation("Here are some recommended programming books:")
            print(table)
        else:
            speak_with_animation("No books found.")
    else:
        speak_with_animation("Failed to connect to the Google Books API.")

if __name__ == "__main__":
    speak_with_animation("Hello! I am your voice-controlled learning assistant.")
    speak_with_animation("How may I assist you today?")
    print_features()

    while True:
        query = take_command().lower()

        if 'features' in query or 'capabilities' in query:
            print_features()
        elif 'trivia quiz' in query:
            trivia_quiz()
        elif 'science facts' in query:
            science_facts()
        elif 'quotes of the day' in query:
            quotes_of_the_day()
        elif 'book recommendations' in query:
            book_recommendations()
        elif 'exit' in query:
            speak_with_animation("Thank you for learning with me. Have a great day!")
            break
        else:
            speak_with_animation("I'm sorry, I didn't understand that. Please try again.")
