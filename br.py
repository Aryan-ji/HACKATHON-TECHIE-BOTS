import subprocess
import cv2
import pytesseract
import pyttsx3

# Initialize the Tesseract OCR engine
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Initialize the pyttsx3 text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

rate = engine.getProperty('rate')
engine.setProperty('rate', 125)

# Variable to store the TTS speech ID
tts_speech_id = None


# Function to perform real-time text recognition and speech synthesis
def process_frame(frame):
    global tts_speech_id  # Access the global TTS speech ID

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Perform text recognition using Tesseract OCR
    text = pytesseract.image_to_string(gray)

    # Print the recognized text
    print("Recognized Text: ", text)

    # Stop the TTS speech from the previous frame if it's still speaking
    if tts_speech_id is not None:
        engine.stop()

    # Speak the recognized text
    engine.say(text)
    engine.runAndWait()


# Function to capture video frames and process them
def capture_video():
    global tts_speech_id  # Access the global TTS speech ID

    # Open the video capture device (0 is typically the default webcam)
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)
    cap.set(cv2.CAP_PROP_FPS, 15)

    while True:
        # Read a frame from the video capture
        ret, frame = cap.read()

        # Display the frame
        cv2.imshow("Real-Time Text-to-Speech", frame)

        # Check if the specified key is pressed
        key = cv2.waitKey(1) & 0xFF
        if key == ord('c'):  # Press 'c' key to capture frame
            # Stop the ongoing speech synthesis
            if tts_speech_id is not None:
                engine.stop()

            # Perform text recognition and speech synthesis on the new frame
            process_frame(frame)

        # Break the loop if 'q' is pressed
        if key == ord('q'):  # Press 'q' key to quit
            break

    # Release the video capture device and close the OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

    # Run ai.py after the program is closed
    subprocess.run(["python", "ai.py"])


# Start capturing and processing video frames
capture_video()
