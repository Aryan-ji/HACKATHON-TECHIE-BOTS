import datetime
import subprocess
import sys

import pyttsx3
import pytz
import requests
import speech_recognition as sr
import wikipedia

engine = pyttsx3.init()
engine.setProperty('rate', 190)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('volume', 1)

api_key = "4cbc3a6b7db914cadda17514b61555c0"
location = 'Patna'

url = f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric'


def speak(text):
    engine.say(text)
    engine.runAndWait()


# change voice
def voice_change(v):
    x = int(v)
    engine.setProperty('voice', voices[x].id)
    speak("done sir")


def checktime(tt):
    hour = datetime.datetime.now().hour
    if "morning" in tt:
        if 6 <= hour < 12:
            speak("Good morning sir")
        else:
            if 12 <= hour < 18:
                speak("it's Good afternoon sir")
            elif 18 <= hour < 24:
                speak("it's Good Evening sir")
            else:
                speak("it's Goodnight sir")
    elif "afternoon" in tt:
        if 12 <= hour < 18:
            speak("it's Good afternoon sir")
        else:
            if 6 <= hour < 12:
                speak("Good morning sir")
            elif 18 <= hour < 24:
                speak("it's Good Evening sir")
            else:
                speak("it's Goodnight sir")
    else:
        speak("it's night sir!")


def wishme():
    speak("Welcome Back")
    hour = datetime.datetime.now().hour
    if 6 <= hour < 12:
        speak("Good Morning sir!")
    elif 12 <= hour < 18:
        speak("Good afternoon sir")
    elif 18 <= hour < 24:
        speak("Good Evening sir")
    else:
        speak("Goodnight sir")

    speak("AI at your service, Please tell me how can i help you?")


def wishme_end():
    speak("signing off")
    hour = datetime.datetime.now().hour
    if 6 <= hour < 12:
        speak("Good Morning")
    elif 12 <= hour < 18:
        speak("Good afternoon")
    elif 18 <= hour < 24:
        speak("Good Evening")
    else:
        speak("Goodnight.. Sweet dreams")
    quit()


# Python3 program to convert
# time into words

# Print Time in words.
def timetoword(h, m):
    nums = ["zero", "one", "two", "three", "four",
            "five", "six", "seven", "eight", "nine",
            "ten", "eleven", "twelve", "thirteen",
            "fourteen", "fifteen", "sixteen",
            "seventeen", "eighteen", "nineteen",
            "twenty", "twenty one", "twenty two",
            "twenty three", "twenty four",
            "twenty five", "twenty six", "twenty seven",
            "twenty eight", "twenty nine"]

    if m == 0:
        return nums[h], "o' clock"

    elif m == 1:
        return "one minute past", nums[h]

    elif m == 59:
        return "one minute to", nums[(h % 12) + 1]

    elif m == 15:
        return "quarter past", nums[h]

    elif m == 30:
        return "half past", nums[h]

    elif m == 45:
        return "quarter to", (nums[(h % 12) + 1])

    elif m <= 30:
        return nums[m], "minutes past", nums[h]

    elif m > 30:
        return (nums[60 - m], "minutes to",
                nums[(h % 12) + 1])


def currentWheater():
    # Send the HTTP GET request
    response = requests.get(url)

    # Parse the JSON response
    data = response.json()

    weather_description = data['weather'][0]['description'].capitalize()
    temperature = data['main']['temp']
    humidity = data['main']['humidity']
    wind_speed = data['wind']['speed']

    weather_paragraph = f"In {location}, the weather is currently {weather_description}. " \
                        f"The temperature is {temperature}°C with a humidity of {humidity}%. " \
                        f"The wind speed is {wind_speed} meters per second."
    return weather_paragraph


# Set the timezone to India
timezone = pytz.timezone('Asia/Kolkata')

# Get the current time in India
current_time = datetime.datetime.now(timezone)

# Format the time as per your requirement
formatted_time_h = current_time.strftime('%H')
formatted_time_m = current_time.strftime('%M')
h = int(formatted_time_h)
m = int(formatted_time_m)


def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 0.5
        # r.adjust_for_ambient_noise(source, 2)
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(query)
        return query
    except Exception as e:
        print(e)
        speak("say that again please...")
        return "none"


def ai():
    # speak("Hi, I'm your AI. How can I help you?")

    while True:
        command = listen().lower()

        if "hello" in command or "hi" in command or "hey" in command:
            speak("Hello! How are you?How can I help you")
        elif "how are you" in command:
            speak("I'm good. Thank you!")
        elif "what's your name" in command:
            speak("I'm an AI created with Python.")
        elif "read book" in command or "red book" in command or "read text" in command or "read text" in command or "recognize text" in command:
            speak("Sure Sir! initializing text to speech")
            subprocess.run(["python", "br.py"])
        elif "listen again" in command:
            speak("listening again")
            ai()
        elif "time" in command or "what is the time now" in command or "current time" in command:
            curTime = timetoword(h, m)
            speak("It's about :")
            speak(curTime)

        elif "on light" in command or "on led" in command or "on bulb" in command:
            requests.get(f'http://172.20.10.3/led?led=Turn+On')
            speak("The Lights Are Turned On")
        elif "off light" in command or "off led" in command or "off bulb" in command or "of light" in command or "of led" in command or "of bulb" in command:
            requests.get(f'http://172.20.10.3/led?led=Turn+Off')
            speak("The Lights Are Turned Off")
        elif "on fan" in command or "on motor" in command or "on cell fan" in command:
            requests.get(f'http://172.20.10.3/motor?motor=Turn+On')
            speak("The Fan is Turned on")
        elif "off fan" in command or "off motor" in command or "off cell fan" in command or "of fan" in command or "of motor" in command or "of cell fan" in command:
            requests.get(f'http://172.20.10.3/motor?motor=Turn+Off')
            speak("The Fan is Turned off")

        elif "current weather" in command or "weather report" in command:
            current_weather = currentWheater()
            speak(current_weather)

        elif "front of me" in command or "detect object" in command or "what is in front of me" in command:
            speak("Detecting Objects...")
            subprocess.run(["python", "oll.py"])
        elif ("hii" in command or "hello" in command or "goodmorning" in command
              or "goodafternoon" in command or "goodnight" in command
              or "morning" in command or "noon" in command or "night" in command):
            command = command.replace("AI", "")
            command = command.replace("hi", "")
            command = command.replace("hello", "")
            if ("morning" in command or "night" in command or "goodnight" in command
                    or "afternoon" in command or "noon" in command):
                checktime(command)
            else:
                speak("what can i do for you")

        elif ('i am done' in command or 'bye bye AI' in command
              or 'go offline AI' in command or 'bye' in command
              or 'nothing' in command):
            wishme_end()

        elif "voice" in command or "change your" in command:
            speak("for female say female and, for male say male")
            q = listen()
            if "female" in q:
                voice_change(1)
            elif "male" in q:
                voice_change(0)
        elif "male" in command or "female" in command:
            if "female" in command:
                voice_change(1)
            elif "male" in command:
                voice_change(0)

        elif ('wikipedia' in command or 'what' in command or 'who' in command
              or 'when' in command or 'where' in command):
            speak("searching...")
            command = command.replace("wikipedia", "")
            command = command.replace("search", "")
            command = command.replace("what", "")
            command = command.replace("when", "")
            command = command.replace("where", "")
            command = command.replace("who", "")
            command = command.replace("is", "")
            result = wikipedia.summary(command, sentences=2)
            print(command)
            print(result)
            speak(result)

        else:
            print("Sorry, I didn't understand that. Can you please repeat?")


if __name__ == "__main__":
    wishme()
    ai()
