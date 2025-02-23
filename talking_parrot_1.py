import speech_recognition as sr
import pyttsx3
import cv2
import threading
import requests
import time
import os
import wikipediaapi
import pygame
import pyjokes
import spotipy
import playsound
import keyboard


# Initialize the recognizer, text-to-speech engine, and Wikipedia API
recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()
wiki_wiki = wikipediaapi.Wikipedia(user_agent="MyPythonApp/1.0", language="en")


# Function to make the assistant speak
def speak(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

# Function to recognize speech
def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I did not understand that.")
            return ""
        except sr.RequestError:
            speak("There is an issue with the speech recognition service.")
            return ""

# Function to search Wikipedia
def search_wikipedia(query):
    page = wiki_wiki.page(query)
    if page.exists():
        return page.summary[:300]
    else:
        return "No information found."

# Function to take a picture
def take_picture():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        speak("I cannot access the webcam.")
        return
    speak("Say 'capture' when you're ready.")
    
    while True:
        command = listen()
        if "capture" in command:
            ret, frame = cap.read()
            if ret:
                cv2.imwrite("picture.jpg", frame)
                speak("Picture taken and saved as picture.jpg")
                cv2.imshow("Captured Image", frame)
                cv2.waitKey(2000)
                cv2.destroyAllWindows()
            break
    cap.release()

# Function to tell a joke
def tell_joke():
    joke = pyjokes.get_joke()
    speak(joke)

# Function to get weather details
def get_weather(city):
    api_key = "84190506d5bf0843188d4a9531d7117c"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(url).json()
    
    if response["cod"] != "404":
        weather = response["weather"][0]["description"]
        temp = round(response["main"]["temp"] - 273.15, 2)
        return f"The weather in {city} is {weather}. The temperature is {temp}°C."
    else:
        return "City not found."

# Function to set a timer
def set_timer(duration):
    def play_alarm():
        pygame.mixer.init()
        pygame.mixer.music.load(r"e:\DISHA\python coding\butter.mp3")  # Load the alarm sound
        pygame.mixer.music.play(-1)  # Play in a loop
        while not keyboard.is_pressed('space'):  # Wait for user to press space
            time.sleep(0.1)
        pygame.mixer.music.stop()  # Stop the alarm when space is pressed

    speak(f"Timer set for {duration} seconds.")
    time.sleep(duration)
    speak("Time's up!")

    alarm_thread = threading.Thread(target=play_alarm)
    alarm_thread.start()

    while not keyboard.is_pressed('space'):
        time.sleep(0.1)

    alarm_thread.join()

# Function to open applications
app_mapping = {
    "notepad": "notepad",
    "calculator": "calc",
    "word": "start winword",
    "powerpoint": "start powerpnt",
    "camera": "start microsoft.windows.camera:",
    "spotify": "start spotify:",
    "chrome": "start chrome.exe"
}

def open_application(app_name):
    if app_name in app_mapping:
        speak(f"Opening {app_name}")
        os.system(app_mapping[app_name])
        
    else:
        speak("Application not found.")

# Function to play a song on Spotify
def play_song(song_name):
    os.system(f"start spotify:search:{song_name}")

# Function to process user commands
def process_command(command):
    if "hello" in command:
        speak("Hello! How can I assist you?")
    elif "your name" in command:
        speak("I am your Talking Parrot assistant.")
    elif "search" in command:
        speak("What do you want to search for?")
        search_query = listen()
        if search_query:
            speak(search_wikipedia(search_query))
    elif "take a picture" in command:
        take_picture()
    elif "joke" in command:
        tell_joke()
    elif "weather" in command:
        speak("Which city?")
        city = listen()
        speak(get_weather(city))
    elif "timer" in command:
        speak("How many seconds?")
        duration = listen()
        if duration.isdigit():
            set_timer(int(duration))
        else:
            speak("Please say a valid number.")
    elif any(app in command for app in app_mapping):
        for app_name in app_mapping.keys():
            if app_name in command:
                open_application(app_name)
                break
    elif "play" in command:
        song_name = command.replace("play", "").strip()
        play_song(song_name)
    elif "exit" in command:
        speak("Goodbye!")
        return False
    else:
        speak("I am not sure how to respond to that.")
    return True

# Main function
def main():
    speak("Hi, I am Talking Parrot. How can I help you?")
    while True:
        command = listen()
        if not process_command(command):
            break

# Run the assistant
if __name__ == "__main__":
    main()
