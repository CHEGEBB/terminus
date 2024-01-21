 #task_automation.py


import os
import subprocess
import pyttsx3
import speech_recognition as sr
from tqdm import tqdm
import requests
from bs4 import BeautifulSoup as HQArena
from tabulate import tabulate
from xml.dom.minidom import parseString
import pandas as pd
import moviepy.editor as editor
from dotenv import load_dotenv

# Initializing pyttsx3 and speech recognition
engine = pyttsx3.init()
recognizer = sr.Recognizer()

# Edamam API Key and App ID
EDAMAM_API_KEY = os.getenv('EDAMAM_API_KEY')
EDAMAM_APP_ID = os.getenv('EDAMAM_APP_ID')

# Function to speak
def speak(audio, voice_id=None):
    engine = pyttsx3.init()

    # Get available voices
    voices = engine.getProperty('voices')

    # Set the voice if specified, otherwise use the default voice
    if voice_id is not None and 0 <= voice_id < len(voices):
        engine.setProperty('voice', voices[voice_id].id)

    engine.say(audio)
    engine.runAndWait()

# Function to take voice command
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

# Function to find all HTML pages
def find_all_html_pages(main_page_url):
    response = requests.get(main_page_url, allow_redirects=True)
    data = HQArena(response.text, 'lxml')
    all_pages = data.find_all('a', itemprop="url")
    return all_pages

# Function to download an image
def download_image(url, url_prefix, count):
    response = requests.get(url, allow_redirects=True)
    data = HQArena(response.text, 'lxml')
    image_url = data.find('a', id="resolution")
    file_postfix = data.find('meta', itemprop="keywords")['content'].replace(" ", "-").replace(",", "")[:20]

    if image_url is not None:
        i_url = image_url['href']
        try:
            response = requests.get(url_prefix + i_url, stream=True)
            total_size_in_bytes = int(response.headers.get('content-length', 0))
            block_size = 1024
            progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)

            with open(f'wallpapers/{count}-{file_postfix}.jpg', 'wb') as file:
                for data in response.iter_content(block_size):
                    progress_bar.update(len(data))
                    file.write(data)
            progress_bar.close()
            if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
                print("ERROR, something went wrong")
        except:
            print("It might be the connection broken :|")

# Function to perform system maintenance and display results in a table
def perform_system_maintenance():
    try:
        # Run disk cleanup
        cleanup_result = subprocess.run(["cleanmgr", "/sagerun:1"], capture_output=True, text=True)

        # Run disk defragmenter
        defrag_result = subprocess.run(["defrag", "/C"], capture_output=True, text=True)

        # Display results in a table
        table = [
            ["Disk Cleanup", cleanup_result.stdout.strip()],
            ["Disk Defragmenter", defrag_result.stdout.strip()]
        ]
        result_table = tabulate(table, headers=["Task", "Result"], tablefmt="pretty")

        # Speak and print the table
        engine.say("System maintenance completed successfully.")
        print(result_table)
    except Exception as e:
        engine.say(f"Error performing system maintenance: {str(e)}")

# Function to tell a joke using JokeAPI
def tell_joke():
    joke_api_url = "https://v2.jokeapi.dev/joke/Any"
    response = requests.get(joke_api_url)
    joke_data = response.json()

    if "joke" in joke_data:
        joke = joke_data["joke"]
        speak(joke)
        print(joke)
    elif "setup" in joke_data and "delivery" in joke_data:
        setup = joke_data["setup"]
        delivery = joke_data["delivery"]
        speak(f"{setup} {delivery}")
        print(f"{setup}\n{delivery}")
    else:
        speak("I'm sorry, I couldn't fetch a joke at the moment.")

# Function to find news headlines using Google News RSS
def get_google_news_result(term, count):
    results = []
    obj = parseString(
        requests.get("http://news.google.com/news?q=%s&output=rss" % term).text
    )
    items = obj.getElementsByTagName("item")
    
    # Storing the Titles
    titles = []
    for item in items[:count]:
        title = ""
        for node in item.childNodes:
            if node.nodeName == "title":
                title = node.childNodes[0].data
        titles.append(title)

    return titles

# Function to get and speak news headlines
def get_and_speak_news(term="latest news", count=5, voice_id=None):
    headlines = get_google_news_result(term, count)
    
    if headlines:
        speak(f"Here are the latest news headlines about {term}:")
        for i, headline in enumerate(headlines):
            speak(f"News {i + 1}: {headline}", voice_id)
            print(f"News {i + 1}: {headline}")
    else:
        speak(f"I'm sorry, I couldn't find any news about {term}.")

# Function to find recipes using Edamam API
def find_recipe(food):
    try:
        # Making the API call
        response = requests.get(f"https://api.edamam.com/search?q={food}&app_id={os.getenv('EDAMAM_APP_ID')}&app_key={os.getenv('EDAMAM_API_KEY')}")
        data = response.json()
        
        # Storing the recipe titles and URLs
        recipe_titles = []
        recipe_urls = []
        for recipe in data['hits']:
            recipe_titles.append(recipe['recipe']['label'])
            recipe_urls.append(recipe['recipe']['url'])
        
        # Creating a dataframe to display the results
        df = pd.DataFrame({
            'Recipe': recipe_titles,
            'URL': recipe_urls
        })
        
        # Displaying the results in a table
        print(tabulate(df, headers='keys', tablefmt='psql'))
        speak("Here are the recipes I found:")
        speak(df.to_string(index=False))
    except Exception as e:
        speak("Something went wrong. Please try again.")
        print(f"Error: {e}")

# Function to convert video to audio
def convert_video_to_audio(video_file, audio_folder):
    try:
        video_clip = editor.VideoFileClip(video_file)
        
        # Creating the 'audio' folder if it doesn't exist
        if not os.path.exists(audio_folder):
            os.makedirs(audio_folder)
        
        audio_path = os.path.join(audio_folder, "converted_audio.mp3")
        video_clip.audio.write_audiofile(audio_path)

        # Voice feedback
        speak("Video converted to audio. You can find the audio file in the 'audio' folder.")
    except Exception as e:
        speak("Something went wrong during the conversion. Please try again.")
        print(f"Error: {e}")

# Main script
if __name__ == "__main__":
    wallpaper_folder = 'wallpapers'
    audio_folder = 'audio'
    
    # Check if 'wallpapers' folder exists, if not, create it
    if not os.path.exists(wallpaper_folder):
        os.makedirs(wallpaper_folder)
        speak("Wallpapers folder created if you would like to download wallpapers. You can now download wallpapers and find them in the wallpapers folder.")

    speak("Hello! Terminus can also automate tasks. I can download wallpapers, perform system maintenance, tell jokes, and find recipes,get latest news and convert video to audio. How may I assist you today?")
    all_pages = find_all_html_pages("https://4kwallpapers.com/random-wallpapers/")
    count = 0

    while True:
        query = take_command().lower()

        if 'download wallpaper' in query:
            speak("Downloading wallpapers. Please wait.")
            for page in all_pages:
                url = page['href']
                download_image(url, "https://4kwallpapers.com", count)
                count += 1
            speak("Wallpapers downloaded successfully and stored in the wallpapers folder.")
        elif 'perform system maintenance' in query:
            speak("Performing system maintenance. Please wait.")
            perform_system_maintenance()
        elif 'tell me a joke' in query or 'hey terminus tell me a joke' in query or 'I am sad' in query:
            tell_joke()

        elif 'find recipe for' in query:
            food = query.split('find recipe for')[1].strip()
            find_recipe(food)
        elif 'keep me updated' in query or 'latest news' in query:
            get_and_speak_news(voice_id=1)  # Set voice_id to the index of the desired voice
        elif 'convert video to audio' in query:
            speak("Sure! Please provide the full path of the video file.")
            video_path = input("Video Path: ")
            convert_video_to_audio(video_path, audio_folder)
        elif 'exit' in query:
            speak("Thank you for using Terminus. Have a great day!")
            break
        else:
            speak("Invalid command. Please try again.")
