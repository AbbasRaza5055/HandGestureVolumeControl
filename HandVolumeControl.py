# Importing required libraries
import cv2  # OpenCV for image processing
import mediapipe as mp  # MediaPipe for hand tracking
import HandTrackingModule as htm  # Custom module for hand tracking
import math  # Math for calculating distance
import numpy as np  # NumPy for interpolation
from ctypes import cast, POINTER  # For handling low-level C interfaces (COM)
from comtypes import CLSCTX_ALL  # COM context constant
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume  # Pycaw for controlling system volume

# Setting the camera frame size
wCam, hCam = 640, 480

# Creating hand detector object with confidence threshold
detector = htm.handDetector(detectionCon=0.7)

# Getting default audio device (speakers)
devices = AudioUtilities.GetSpeakers()

# Activating the audio endpoint interface
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)

# Casting the interface pointer to a usable object
volume = cast(interface, POINTER(IAudioEndpointVolume))

# Getting the min and max volume range
volRange = volume.GetVolumeRange()
minVol = volRange[0]  # Minimum volume
maxVol = volRange[1]  # Maximum volume

# Initial volume variables
vol = 0
volBar = 400
volPer = 0

# Start capturing video from webcam
cap = cv2.VideoCapture(0)
cap.set(3, wCam)  # Set width
cap.set(4, hCam)  # Set height

# Infinite loop for real-time processing
while True:
    success, img = cap.read()  # Read frame from webcam

    img = detector.findHands(img)  # Detect and draw hands
    lmList = detector.findPosition(img, draw=False)  # Get list of landmark positions

    if len(lmList) != 0:
        # Get coordinates of thumb tip (id 4) and index finger tip (id 8)
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]

        # Calculate center between thumb and index
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        # Draw circles and line between thumb and index
        cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

        # Calculate Euclidean distance between fingers
        length = math.hypot(x2 - x1, y2 - y1)

        # Convert length to volume level using interpolation
        vol = np.interp(length, [50, 200], [minVol, maxVol])
        volBar = np.interp(length, [50, 200], [400, 150])  # For visual bar
        volPer = np.interp(length, [50, 250], [0, 100])  # Percentage

        # Print distance and volume for debugging
        print(int(length), vol)

        # Set system volume
        volume.SetMasterVolumeLevel(vol, None)

        # If fingers are close, draw green dot (mute zone)
        if length < 50:
            cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)

        # Draw volume bar and percentage text
        cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
        cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 0), cv2.FILLED)
        cv2.putText(img, f'{int(volPer)}%', (40, 450),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0))

    # Show the final image
    cv2.imshow("image", img)

    # Break loop if 'q' is pressed
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

# Release the camera and destroy all OpenCV windows
cap.release()
cv2.destroyAllWindows()
