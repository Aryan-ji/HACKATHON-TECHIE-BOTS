import subprocess

import cv2
import pyttsx3
import time

thres = 0.45  # Threshold to detect object

cap = cv2.VideoCapture(1)
cap.set(3, 640)
cap.set(4, 480)
cap.set(10, 70)

classNames = []
classFile = 'coco.names'
with open(classFile, 'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')

configPath = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
weightsPath = 'frozen_inference_graph.pb'

net = cv2.dnn_DetectionModel(weightsPath, configPath)
net.setInputSize(300, 300)  # Reduce input size to 300x300
net.setInputScale(1.0 / 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

# Initialize TTS engine
engine = pyttsx3.init()

detect_objects = False
tts_duration = 1  # Duration in seconds for TTS
tts_start_time = 0

def toggle_object_detection():
    global detect_objects
    global tts_start_time

    detect_objects = not detect_objects

    if detect_objects:
        tts_start_time = time.time()
        print("Object detection activated")
    else:
        tts_start_time = 0
        print("Object detection deactivated")

def perform_tts(objects):
    for obj in objects:
        detected_object = obj.upper()
        engine.say(detected_object)
        engine.runAndWait()

while True:
    success, img = cap.read()
    img = cv2.resize(img, (640, 480))  # Reduce frame size to 640x480
    classIds, confs, bbox = net.detect(img, confThreshold=thres)
    print(classIds, bbox)

    if detect_objects and len(classIds) != 0:
        objects = [classNames[classId - 1] for classId in classIds.flatten()]
        current_time = time.time()
        if current_time - tts_start_time <= tts_duration:
            perform_tts(objects)
        else:
            detect_objects = False

    # Comment out the lines below if you don't need visualizations
    for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
        cv2.rectangle(img, box, color=(0, 255, 0), thickness=2)
        cv2.putText(img, classNames[classId - 1].upper(), (box[0] + 10, box[1] + 30),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(img, str(round(confidence * 100, 2)), (box[0] + 200, box[1] + 30),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Output", img)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

    if key == ord('c') and not detect_objects:
        toggle_object_detection()

cap.release()
cv2.destroyAllWindows()
subprocess.run(["python", "ai.py"])
