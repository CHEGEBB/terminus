import requests
import json
import random
import pyttsx3
import speech_recognition as sr
from googleapiclient.discovery import build

QUOTES_API_KEY = '5puUUckdHEGxeyzdyHuDhaP4FN0EGfR3RGC1OkwX'
NASA_API_KEY = '7k4b22cjrbbjg29R1VBDzEfebZkO2BRBim3mtUTX'
GOOGLE_BOOKS_API_KEY = 'AIzaSyDXn8j-bYJoojOqy303i4oGU_PKVTRhzzU'

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

# Placeholder for language learning API
def language_learning():
    # Implement language learning using an external API
    # Example: Duolingo API - https://developers.duolingo.com/docs/
    pass

# Placeholder for trivia quiz API
def trivia_quiz():
    # Implement trivia quiz using an external API
    # Example: Open Trivia Database API - https://opentdb.com/api_config.php
    
    # Open Trivia Database API endpoint
    api_url = "https://opentdb.com/api.php?amount=15"

    # Fetching trivia questions
    response = requests.get(api_url)
    if response.status_code == 200:
        trivia_data = response.json()
        if trivia_data["response_code"] == 0:
            questions = trivia_data["results"]
            speak("Welcome to Trivia Quiz. Get ready for some questions!")
            speak("I will read out a question, and you can answer by saying the corresponding option number.")
            display_trivia_questions(questions)
        else:
            speak("Failed to fetch trivia questions.")
    else:
        speak("Failed to connect to the Open Trivia Database.")

def display_trivia_questions(questions):
    score = 0
    recognizer = sr.Recognizer()

    for index, question in enumerate(questions, start=1):
        speak(f"Question {index}: {question['question']}")
        options = question['incorrect_answers'] + [question['correct_answer']]
        random.shuffle(options)

        for i, option in enumerate(options, start=1):
            speak(f"Option {i}: {option}")

        speak("Your answer:")
        user_answer = take_trivia_answer(recognizer)
        correct_answer = options.index(question['correct_answer']) + 1

        if user_answer == correct_answer:
            speak("Correct!")
            score += 1
        else:
            speak(f"Wrong! The correct answer is {correct_answer}.")
    
    speak(f"Quiz completed! Your score: {score}/{len(questions)}")

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
                speak("Invalid response. Please try again.")
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that. Can you please repeat?")
        except sr.RequestError:
            speak("I'm having trouble accessing the microphone. Please check your connection.")

# Placeholder for programming challenges API
def programming_challenges():
    # Implement programming challenges using an external API
    # Example: HackerRank API - https://www.hackerrank.com/api
    pass

# Placeholder for historical facts API
def historical_facts():
    # Implement historical facts using an external API
    # Example: History API - https://historyapi.dev/
    pass

# Science Facts using NASA API
def science_facts():
    # Implement science facts using an external API
    # Example: NASA Open APIs - https://api.nasa.gov/
    
    # NASA API endpoint for APOD (Astronomy Picture of the Day)
    nasa_api_url = f"https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}"

    # Fetching today's astronomy picture and facts
    response = requests.get(nasa_api_url)
    if response.status_code == 200:
        nasa_data = response.json()
        speak("Here is today's astronomy picture of the day.")
        speak(nasa_data['explanation'])
    else:
        speak("Failed to connect to the NASA API.")

# Placeholder for math problems API
def math_problems():
    # Implement math problems using an external API
    # Example: Math Exchange API - https://api.mathexchange.io/
    pass

# Quotes of the Day using They Said So Quotes API
def quotes_of_the_day():
    # Implement quotes of the day using an external API
    # Example: They Said So Quotes API - https://quotes.rest/
    
    # They Said So Quotes API endpoint
    quotes_api_url = f"https://quotes.rest/qod?category=inspire&api_key={QUOTES_API_KEY}"

    # Fetching quote of the day
    response = requests.get(quotes_api_url)
    if response.status_code == 200:
        quotes_data = response.json()
        quote_content = quotes_data['contents']['quotes'][0]['quote']
        speak(f"Here is the inspirational quote of the day: {quote_content}")
    else:
        speak("Failed to connect to the They Said So Quotes API.")

# Google Books API for Book Recommendations
def book_recommendations():
    # Implement book recommendations using an external API
    # Example: Google Books API - https://developers.google.com/books
    
    # Google Books API endpoint
    google_books_api = build('books', 'v1', developerKey=GOOGLE_BOOKS_API_KEY)

    # Fetching book recommendations
    response = google_books_api.volumes().list(q='programming', orderBy='relevance').execute()
    
    if 'items' in response:
        books = response['items'][:5]  # Displaying the top 5 book recommendations
        speak("Here are some recommended programming books:")
        for book in books:
            title = book['volumeInfo']['title']
            author = ', '.join(book['volumeInfo']['authors'])
            speak(f"{title} by {author}")
    else:
        speak("Failed to connect to the Google Books API.")

# Placeholder for geography quiz API
def geography_quiz():
    # Implement geography quiz using an external API
    # Example: REST Countries API - https://restcountries.com/v3.1/all
    pass

if __name__ == "__main__":
    speak("Hello! I am your voice-controlled learning assistant.")
    speak("How may I assist you today?")

    while True:
        query = take_command().lower()

        if 'trivia quiz' in query:
            trivia_quiz()
        elif 'science facts' in query:
            science_facts()
        elif 'quotes of the day' in query:
            quotes_of_the_day()
        elif 'book recommendations' in query:
            book_recommendations()
        elif 'exit' in query:
            speak("Thank you for learning with me. Have a great day!")
            break
        else:
            speak("I'm sorry, I didn't understand that. Please try again.")
