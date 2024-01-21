import requests
import speech_recognition as sr
import pyttsx3
import uuid
import os

# Constants for Azure Translator API
subscription_key = os.getenv("AZURE_TRANSLATOR_API_KEY")
endpoint = "https://api.cognitive.microsofttranslator.com/"

# Initialize text-to-speech engine
engine = pyttsx3.init()

def speak(text, voice_id=None):
    """Speaks the given text using text-to-speech."""
    if voice_id:
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[voice_id].id)
    engine.say(text)
    engine.runAndWait()

def translate_text(text, from_lang, to_lang):
    """Translates text using Azure Translator API."""
    headers = {
    'Ocp-Apim-Subscription-Key': os.getenv("AZURE_TRANSLATOR_API_KEY"),
    'Content-type': 'application/json',
    'X-ClientTraceId': str(uuid.uuid4())
             }

    params = {
        'api-version': '3.0',
        'from': from_lang,
        'to': to_lang
    }
    body = [{'text': text}]

    response = requests.post(endpoint + 'translate', headers=headers, params=params, json=body)
    response.raise_for_status()  # Raise an exception for error responses
    return response.json()[0]['translations'][0]['text']

def recognize_speech():
    """Recognizes speech using the microphone."""
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return ""

def main():
    speak("Welcome to the voice-based language translator.")

    while True:
        speak("Please specify the language you want to translate from.")
        from_lang = recognize_speech()

        speak("Please specify the language you want to translate to.")
        to_lang = recognize_speech()

        speak("Please say the words or sentences you want to translate.")
        text = recognize_speech()

        try:
            translated_text = translate_text(text, from_lang, to_lang)
            speak("Here's the translation: " + translated_text)

            speak("Would you like to hear the translation again?")
            repeat_translation = recognize_speech()
            if "yes" in repeat_translation.lower():
                speak("Translation: " + translated_text)

        except Exception as e:
            print(f"Translation error: {e}")
            speak("Sorry, an error occurred during translation.")

        speak("Would you like to translate something else?")
        continue_translation = recognize_speech()
        if "no" in continue_translation.lower():
            break

if __name__ == "__main__":
    main()
