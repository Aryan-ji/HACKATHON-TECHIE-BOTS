import speech_recognition as sr
import requests

# Define the ESP32 IP address and LED control endpoints
esp32_ip = '192.168.92.222'  # Replace with your ESP32 IP address
led_on_url = f'http://{esp32_ip}/H'
led_off_url = f'http://{esp32_ip}/L'

# Initialize the speech recognition recognizer
r = sr.Recognizer()

# Function to process voice commands and control the LED
def process_command(command):
    if 'turn on' in command:
        requests.get(led_on_url)
        print("LED turned on.")
    elif 'turn off' in command:
        requests.get(led_off_url)
        print("LED turned off.")
    else:
        print("Unknown command.")

# Function to listen for voice commands
def listen():
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio)
        print(f"You said: {command}")
        process_command(command.lower())  # Process the recognized command
    except sr.UnknownValueError:
        print("Sorry, I didn't understand that.")
    except sr.RequestError as e:
        print(f"Request error: {str(e)}")

# Main program loop
while True:
    listen()
