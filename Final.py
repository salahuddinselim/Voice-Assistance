import speech_recognition as sr
import pyttsx3
import pyjokes
import os
from googleapiclient.discovery import build

API_KEY = "AIzaSyByJe_5wdv9c465RdO1TOugSvJ7wb1Bcxw"  
SEARCH_ENGINE_ID = "d1a7cc593c66040d2"


engine = pyttsx3.init()

def speak(text):
    
    engine.say(text)
    engine.runAndWait()

def listen():
    
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that. Can you repeat?")
            return None
        except sr.RequestError:
            speak("Network error. Please check your connection.")
            return None

def open_app(app_name):
    apps = {
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        "command prompt": "cmd.exe",
        "edge": "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
        "vs code" : "C:\\Users\\Lenovo\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe" 
    }

    if app_name in apps:
        speak(f"Opening {app_name}.")
        os.startfile(apps[app_name])
    else:
        speak(f"Sorry, I don't have a command to open {app_name}.")

def close_app(app_name):
    
    processes = {
        "notepad": "notepad.exe",
        "calculator": "Calculator.exe",
        "chrome": "chrome.exe",
        "command prompt": "cmd.exe",
        "edge": "msedge.exe",
        "vs code" : "Code.exe"
    }

    if app_name in processes:
        speak(f"Closing {app_name}.")
        os.system(f"taskkill /f /im {processes[app_name]}")
    else:
        speak(f"Sorry, I couldn't find {app_name} running.")

def tell_joke():
    
    joke = pyjokes.get_joke()
    print(f"Joke: {joke}")
    speak(joke)

def search_web(query):
    speak(f"Searching for {query} on Google.")
    
    
    service = build("customsearch", "v1", developerKey=API_KEY)
    result = service.cse().list(q=query, cx=SEARCH_ENGINE_ID).execute()

    if 'items' in result:
        top_result = result['items'][0]
        title = top_result.get('title')
        link = top_result.get('link')
        snippet = top_result.get('snippet')
        
        
        speak(f"Here's the top result: {title}. {snippet}. Opening in your browser.")
        print(f"\nTitle: {title}\nSnippet: {snippet}\nLink: {link}\n")
        
        os.system(f"start {link}")
    else:
        speak("I couldn't find any results.")

def set_reminder(task):
    reminders_file = "reminders.txt"
    
    with open(reminders_file, "a") as file:
        file.write(task + "\n")

    speak(f"Reminder set for: {task}. I've saved it.")

def read_reminders():
    reminders_file = "reminders.txt"

    if os.path.exists(reminders_file):
        with open(reminders_file, "r") as file:
            reminders = file.readlines()
            if reminders:
                speak("Here are your reminders:")
                for i, reminder in enumerate(reminders, start=1):
                    reminder = reminder.strip()
                    print(f"{i}. {reminder}")
                    speak(f"{i}. {reminder}")
            else:
                speak("You have no reminders.")
    else:
        speak("You have no saved reminders.")

def process_command(command):
    if "search for" in command:
        search_query = command.replace("search for", "").strip()
        search_web(search_query)

    elif "set a reminder" in command:
        reminder = command.replace("set a reminder", "").strip()
        set_reminder(reminder)

    elif "read my reminders" in command:
        read_reminders()

    elif "tell me a joke" in command:
        tell_joke()

    elif "open" in command:
        app_name = command.replace("open", "").strip()
        open_app(app_name)

    elif "close" in command:
        app_name = command.replace("close", "").strip()
        close_app(app_name)

    elif "exit" in command or "quit" in command:
        speak("Goodbye!")
        exit()

    else:
        speak("I'm sorry, I didn't understand that command.")


if __name__ == "__main__":
    speak("Hello, This is Infernape. How can I help you today?")
    while True:
        user_command = listen()
        if user_command:
            process_command(user_command)
