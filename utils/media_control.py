import os
import webbrowser
import urllib.request
import pyttsx3
import speech_recognition as sr
import vlc
import pafy
import re

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

# Function to search for local audio mp3 files
def search_audio():
    speak("What do you want to search?")
    query = take_command()
    for root, dirs, files in os.walk("C:\\"):
        for file in files:
            if query in file:
                print(os.path.join(root, file))
                speak("File found")
                break
        else:
            continue
        break
    else:
        speak("File not found")

# Function to search for local video mp4 files
def search_video():
    speak("What do you want to search?")
    query = take_command()
    for root, dirs, files in os.walk("C:\\"):
        for file in files:
            if query in file:
                print(os.path.join(root, file))
                speak("File found")
                break
        else:
            continue
        break
    else:
        speak("File not found")

# Function to play audio from vlc media player if the audio file is present locally
def play_audio():
    speak("What do you want to play?")
    query = take_command()
    for root, dirs, files in os.walk("C:\\"):
        for file in files:
            if query in file:
                print(os.path.join(root, file))
                speak("Playing audio")
                audio = vlc.MediaPlayer(os.path.join(root, file))
                audio.play()
                break
        else:
            continue
        break
    else:
        speak("File not found")

# Function to play video from vlc media player if the video file is present locally
def play_video():
    speak("What do you want to play?")
    query = take_command()
    for root, dirs, files in os.walk("C:\\"):
        for file in files:
            if query in file:
                print(os.path.join(root, file))
                speak("Playing video")
                video = vlc.MediaPlayer(os.path.join(root, file))
                video.play()
                break
        else:
            continue
        break
    else:
        speak("File not found")

# Function to play audio from YouTube using YouTube v3 API and VLC Python module
def play_youtube_audio():
    speak("What do you want to play on YouTube?")
    query = take_command()
    url = "https://www.youtube.com/results?search_query=" + query
    html = urllib.request.urlopen(url)
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    
    if video_ids:
        url = "https://www.youtube.com/watch?v=" + video_ids[0]
        video = pafy.new(url)
        best_audio = video.getbestaudio()
        play_url = best_audio.url
        speak("Playing audio from YouTube")
        audio_player = vlc.MediaPlayer(play_url)
        audio_player.play()
    else:
        speak("No videos found on YouTube")

# Function to play video from YouTube using YouTube v3 API and VLC Python module
def play_youtube_video():
    speak("What do you want to play on YouTube?")
    query = take_command()
    url = "https://www.youtube.com/results?search_query=" + query
    html = urllib.request.urlopen(url)
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    
    if video_ids:
        url = "https://www.youtube.com/watch?v=" + video_ids[0]
        video = pafy.new(url)
        best_video = video.getbest()
        play_url = best_video.url
        speak("Playing video from YouTube")
        video_player = vlc.MediaPlayer(play_url)
        video_player.play()
    else:
        speak("No videos found on YouTube")

# Function to pause audio or video from vlc media player
def pause():
    speak("Pausing")
    vlc.MediaPlayer.pause()

# Function to resume audio or video from vlc media player
def resume():
    speak("Resuming")
    vlc.MediaPlayer.play()

# Function to stop audio or video from vlc media player
def stop():
    speak("Stopping")
    vlc.MediaPlayer.stop()

# Function to play next audio or video from vlc media player
def next_track():
    speak("Playing next")
    vlc.MediaPlayer.next()

# Function to play previous audio or video from vlc media player
def previous_track():
    speak("Playing previous")
    vlc.MediaPlayer.previous()

# Function to increase volume of audio or video from vlc media player
def volume_up():
    speak("Increasing volume")
    vlc.MediaPlayer.audio_set_volume(100)

# Function to decrease volume of audio or video from vlc media player
def volume_down():
    speak("Decreasing volume")
    vlc.MediaPlayer.audio_set_volume(0)

# Function to mute audio or video from vlc media player
def mute():
    speak("Muting")
    vlc.MediaPlayer.audio_set_volume(0)

# Function to unmute audio or video from vlc media player
def unmute():
    speak("Unmuting")
    vlc.MediaPlayer.audio_set_volume(100)

# Function to restart audio or video from vlc media player
def restart():
    speak("Restarting")
    vlc.MediaPlayer.set_time(0)

# Function to replay audio or video from vlc media player
def replay():
    speak("Replaying")
    vlc.MediaPlayer.set_time(0)

# Function to start audio or video from vlc media player
def start():
    speak("Starting")
    vlc.MediaPlayer.set_time(0)

# Function to begin audio or video from vlc media player
def begin():
    speak("Beginning")
    vlc.MediaPlayer.set_time(0)

# Function to execute the command
def execute_command(args):
    if args[1] == "search":
        if args[2] == "audio":
            search_audio()
        elif args[2] == "video":
            search_video()
        else:
            speak("Invalid command")
    elif args[1] == "play":
        if args[2] == "audio":
            play_audio()
        elif args[2] == "video":
            play_video()
        elif args[2] == "youtube":
            if args[3] == "audio":
                play_youtube_audio()
            elif args[3] == "video":
                play_youtube_video()
            else:
                speak("Invalid command")
        else:
            speak("Invalid command")
    elif args[1] == "pause":
        pause()
    elif args[1] == "resume":
        resume()
    elif args[1] == "stop":
        stop()
    elif args[1] == "next":
        next_track()
    elif args[1] == "previous":
        previous_track()
    elif args[1] == "volume":
        if args[2] == "up":
            volume_up()
        elif args[2] == "down":
            volume_down()
        else:
            speak("Invalid command")
    elif args[1] == "mute":
        mute()
    elif args[1] == "unmute":
        unmute()
    elif args[1] == "restart":
        restart()
    elif args[1] == "replay":
        replay()
    elif args[1] == "start":
        start()
    elif args[1] == "begin":
        begin()
    else:
        speak("Invalid command")

# Main function
if __name__ == "__main__":
    speak("Hello! I am Terminus, your terminal voice assistant.")
    speak("How may I assist you?")

    while True:
        query = take_command().lower()
        if 'search' in query:
            execute_command(query.split())
        elif 'play' in query:
            execute_command(query.split())
        elif 'pause' in query:
            execute_command(query.split())
        elif 'resume' in query:
            execute_command(query.split())
        elif 'stop' in query:
            execute_command(query.split())
        elif 'next' in query:
            execute_command(query.split())
        elif 'previous' in query:
            execute_command(query.split())
        elif 'volume' in query:
            execute_command(query.split())
        elif 'mute' in query:
            execute_command(query.split())
        elif 'unmute' in query:
            execute_command(query.split())
        elif 'restart' in query:
            execute_command(query.split())
        elif 'replay' in query:
            execute_command(query.split())
        elif 'start' in query:
            execute_command(query.split())
        elif 'begin' in query:
            execute_command(query.split())
        elif 'exit' in query:
            speak("Thank you for using Terminus. Have a nice day!")
            exit()
        else:
            speak("Invalid command")
