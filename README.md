# Terminus - Your Voice-Controlled Terminal Assistant 🎙️🤖

Terminus is a Python-based voice-controlled terminal assistant designed to make your interactions with the terminal more intuitive and engaging. With Terminus, you can perform a variety of tasks using just your voice, from opening websites to executing terminal commands.

**Note: Terminus is still under development! Some features might not be fully implemented, and improvements are being actively worked on. Feel free to contribute and enhance the project!**

## Features 🚀

- **Voice Recognition:** Terminus uses the `speech_recognition` library to capture voice input, making it easy to interact with the terminal using spoken commands.

- **Text-to-Speech:** The assistant responds to your commands with natural-sounding speech through the `pyttsx3` library, providing a seamless user experience.

- **Open Websites:** Terminus can open popular websites like Google, YouTube, Gmail, GitHub, Stack Overflow, and WhatsApp with just a voice command.

- **Execute Terminal Commands:** Perform various terminal operations such as creating directories, removing files, listing files, copying/moving files and directories, renaming files/directories, and more.

- **Dynamic Command Execution:** Terminus dynamically imports and executes commands based on your voice input, making it extensible and customizable.

## Getting Started 🚦

1. **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/terminus.git
    cd terminus
    ```

2. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Run Terminus:**
    ```bash
    python terminus.py
    ```

## Usage 🗣️

- **Wake-Up Command:** Start the assistant by saying "Hello Terminus."

- **Open Websites:** Command Terminus to open websites like Google, YouTube, etc.

- **Execute Terminal Commands:** Perform various terminal operations by stating commands like "Make a directory," "List files," etc.

- **Configure Voice Commands:** Use the configure voice commands command to customize voice commands through the JSON configuration file.

## Contributing 🤝

Contributions are welcome! If you have ideas for improvements or new features, feel free to open an issue or submit a pull request.

**Written by CHEGEBB** 🖋️

**Acknowledgements 🙌:**
Special thanks to the creators of `speech_recognition` and `pyttsx3` for their fantastic libraries.

Happy coding with Terminus! 🚀🔊
