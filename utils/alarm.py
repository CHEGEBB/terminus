import datetime
import winsound                      # pip install playsound
import pyttsx3
import speech_recognition as sr

class VoiceAlarm:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.recognizer = sr.Recognizer()

    def speak(self, audio):
        self.engine.say(audio)
        self.engine.runAndWait()

    def listen(self):
        with sr.Microphone() as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)

        try:
            print("Recognizing...")
            query = self.recognizer.recognize_google(audio, language='en-in')
            print(f"You said: {query}\n")
            return query.lower()
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            return "None"
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return "None"

    def set_alarm(self):
        self.speak("What time do you want to set the alarm? For example, set alarm for 9:30 AM")
        alarm_time = self.listen()

        if 'set alarm' in alarm_time:
            self.speak("Please specify the time for the alarm.")
            alarm_time = self.listen()
        
        if 'alarm' in alarm_time:
            alarm_time = alarm_time.replace('alarm', '')
            alarm_time = alarm_time.strip()

            try:
                altime = datetime.datetime.strptime(alarm_time, "%I:%M %p")
                altime = altime.strftime("%H:%M")
                self.speak(f"Alarm is set for {alarm_time}")
                self.start_alarm(altime)
            except ValueError:
                self.speak("Sorry, I couldn't understand the time. Please try again.")

    def start_alarm(self, timing):
        Hr_real, Min_real = map(int, timing.split(':'))

        while True:
            if Hr_real == datetime.datetime.now().hour and Min_real == datetime.datetime.now().minute:
                self.speak("Alarm is Ringing...")
                winsound.PlaySound('SystemAsterisk', winsound.SND_LOOP)
            elif Min_real < datetime.datetime.now().minute:
                winsound.PlaySound(None, winsound.SND_PURGE)
                break

if __name__ == '__main__':
    alarm_system = VoiceAlarm()
    alarm_system.set_alarm()
