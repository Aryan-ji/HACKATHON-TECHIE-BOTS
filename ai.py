import datetime
import subprocess

import pyttsx3
import pytz
import requests
import speech_recognition as sr

engine = pyttsx3.init()


def speak(text):
    engine.say(text)
    engine.runAndWait()


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
        # r.adjust_for_ambient_noise(source, 2)
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio)
        print(query)
        return query
    except Exception as e:
        print(e)
        return ""


def ai():
    speak("Hi, I'm your AI. How can I help you?")

    while True:
        command = listen().lower()

        if "hello" in command or "hi" in command or "hey" in command:
            speak("Hello! How are you?How can I help you")
        elif "how are you" in command:
            speak("I'm good. Thank you!")
        elif "what's your name" in command:
            speak("I'm an AI created with Python.")
        elif "read book" in command:
            speak("initializing text to speech")
            subprocess.run(["python", "br.py"])
        elif "listen again" in command:
            speak("listening again")
            ai()
        elif "time" in command or "what is the time now" in command or "current time" in command:
            curTime = timetoword(h, m)
            speak("It's about :")
            speak(curTime)
        elif "goodbye" in command or "bye" in command or "exit" in command:
            speak("Goodbye! Have a great day!")
        elif "on light" in command or "on led" in command or "on bulb" in command:
            requests.get(f'http://172.20.10.3/H')
            speak("The Lights Are Turned On")
        elif "off light" in command or "off led" in command or "off bulb" in command:
            requests.get(f'http://172.20.10.3/L')
            speak("The Lights Are Turned Off")

        else:
            print("Sorry, I didn't understand that. Can you please repeat?")


if __name__ == "__main__":
    ai()
