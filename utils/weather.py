import requests
import time
import speech_recognition as sr
import pyttsx3
from rich.console import Console
from rich.progress import Progress
from tabulate import tabulate

console = Console()

def get_weather(api_key, city, units="metric"):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": units,
    }

    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        console.print(f"[red]Error fetching weather data: {e}[/red]")
        return None

def get_forecast(api_key, city, units="metric"):
    base_url = "http://api.openweathermap.org/data/2.5/forecast"
    params = {
        "q": city,
        "appid": api_key,
        "units": units,
    }

    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        console.print(f"[red]Error fetching forecast data: {e}[/red]")
        return None

def display_loading_animation():
    with Progress() as progress:
        task = progress.add_task("[cyan]Fetching weather data...", total=10)
        while not progress.finished:
            progress.update(task, advance=1)
            time.sleep(0.1)

def display_weather(weather_data, units):
    if weather_data is None:
        return

    if "cod" in weather_data and weather_data["cod"] == "404":
        console.print("[red]City not found. Please check the city name.[/red]")
        return

    city = weather_data.get("name", "Unknown City")
    temperature = weather_data["main"]["temp"] if "main" in weather_data else "Unknown Temperature"
    wind_speed = weather_data["wind"]["speed"] if "wind" in weather_data else "Unknown Wind Speed"
    rain_volume = weather_data["rain"]["1h"] if "rain" in weather_data else "Unknown Rain Volume"
    
    unit_label = "C" if units == "metric" else "F"
    weather_table = [
        ["City", city],
        ["Temperature", f"{temperature}°{unit_label}"],
        ["Wind Speed", f"{wind_speed} m/s"],
        ["Rain Volume (last 1h)", f"{rain_volume} mm"],
    ]

    console.print(tabulate(weather_table, tablefmt="fancy_grid"))

def display_forecast(forecast_data, units):
    if forecast_data is None:
        return

    forecast_table = []
    for entry in forecast_data["list"]:
        timestamp = entry["dt_txt"]
        temperature = entry["main"]["temp"]
        description = entry["weather"][0]["description"]

        unit_label = "C" if units == "metric" else "F"
        forecast_table.append([timestamp, f"{temperature}°{unit_label}", description])

    console.print("\n[bold cyan]Forecast for Tomorrow:[/bold cyan]")
    console.print(tabulate(forecast_table, headers=["Timestamp", "Temperature", "Description"], tablefmt="fancy_grid"))

def welcome_message():
    text_to_speech("Welcome to the Weather App!")
    text_to_speech("Say the city name to get the current weather.")
    text_to_speech("Temperature, wind speed, rain volume, and forecast for tomorrow will be displayed.")

    console.print("[bold cyan]Welcome to Weather App![/bold cyan]")
    console.print("Say the city name to get the current weather.")
    console.print("Temperature, wind speed, rain volume, and forecast for tomorrow will be displayed.")

def recognize_speech():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        text_to_speech("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text_to_speech("Recognizing...")
        query = recognizer.recognize_google(audio).lower()
        text_to_speech(f"You said: {query}")
        return query
    except sr.UnknownValueError:
        text_to_speech("[red]Sorry, I couldn't understand the audio. Please try again.[/red]")
        return None
    except sr.RequestError as e:
        text_to_speech(f"[red]Could not request results from Google Speech Recognition service; {e}[/red]")
        return None

def text_to_speech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def main():
    api_key = "aaf06191d54d5d7adcf736c7380775ce"  # Replace with your actual API key

    welcome_message()

    while True:
        city_name = recognize_speech()

        if city_name:
            display_loading_animation()
            weather_data = get_weather(api_key, city_name)
            forecast_data = get_forecast(api_key, city_name)

            display_weather(weather_data, "metric")
            display_forecast(forecast_data, "metric")

            response_text = (
                f"The current weather in {city_name} is {weather_data['main']['temp']} degrees Celsius with "
                f"{weather_data['weather'][0]['description']}."
            )
            text_to_speech(response_text)

if __name__ == "__main__":
    main()
