import platform
import psutil
from termcolor import colored
import pyttsx3
from tabulate import tabulate

class SystemInfo:
    def __init__(self):
        self.engine = pyttsx3.init()

    def speak(self, audio):
        self.engine.say(audio)
        self.engine.runAndWait()

    def display_system_info(self):
        # Get additional system information
        additional_info = {
            "Python Version": platform.python_version(),
            "Machine": platform.machine(),
            "System Architecture": platform.architecture(),
            "Processor Architecture": platform.processor(),
            "RAM Usage": f"{psutil.virtual_memory().percent}%",
            "Disk Usage": f"{psutil.disk_usage('/').percent}%",
            "Battery Percentage": self.get_battery_percentage(),
        }

        # Merge the dictionaries
        system_info = {**self.get_base_system_info(), **additional_info}

        # Displaying animated system info
        self.speak("Displaying system information.")
        self.display_table(system_info)

    def get_base_system_info(self):
        return {
            "OS": platform.system(),
            "OS Version": platform.version(),
            "CPU": platform.processor(),
            "RAM": f"{psutil.virtual_memory().total / (1024 ** 3):.2f} GB",
            "Disk Space": f"{psutil.disk_usage('/').total / (1024 ** 3):.2f} GB",
        }

    def get_battery_percentage(self):
        battery = psutil.sensors_battery()
        if battery:
            return f"{battery.percent}%"
        else:
            return "N/A"

    def display_table(self, data):
        headers = ["Category", "Information"]
        rows = [[colored(category, "cyan"), info] for category, info in data.items()]
        table = tabulate(rows, headers, tablefmt="grid")
        print(table)

if __name__ == "__main__":
    sys_info = SystemInfo()
    sys_info.display_system_info()
