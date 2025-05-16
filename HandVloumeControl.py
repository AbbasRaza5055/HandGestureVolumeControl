import cv2
import mediapipe as mp
import HandTrackingModule as htm
import math
import numpy as np
from ctypes import cast, POINTER  #Built in python library that allow you to call function and use data types from shared libararies and DLL(c and c++)
from comtypes import CLSCTX_ALL  #Python library for working with Windows COM interfaces.CLSCTX: A constant that tells Windows to activate a COM object using any method available
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume #Python Core Audio Window.  AudioUtilities: get a list of Audio devices
#Size of the frame
wCam, hCam = 640,480
#object created of the handDetector module
detector = htm.handDetector(detectionCon=0.7)

#Used for controlling the volume of the device
devices = AudioUtilities.GetSpeakers() #AudioUtilities class to get list of audio devices
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
#IAudioEndpointVolume: Provides method to control the volume e.g GetVolumeRange, SetMasterVolumeLevel etc
#-iid-: The unique interface ID (GUID) used to identify this COM interface
volume = cast( interface, POINTER(IAudioEndpointVolume))  #interface is raw COM obj
#converting a generic COM interface pointer into a usable Python object that lets you control your system’s volume.
volRange = volume.GetVolumeRange()# It returns a tuple of three values: (minVolume, maxVolume, increment)
minVol = volRange[0]
maxVol = volRange[1]
vol = 0
volBar = 400
volPer = 0

#Capture the frame of video
cap = cv2.VideoCapture(0)
cap.set(3,wCam) #setting the width of the frame OpenCV defines constants for each video property 3 for width
cap.set(4,hCam) #setting the height of the frame 4 constant for height

while True:
    success, img = cap.read()

    img = detector.findHands(img)
    lmList = detector.findPosition(img,draw = False)
    if len(lmList) != 0:
        # print(lmList[4],lmList[8])

        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1+x2)//2, (y1+y2)//2    #For finding the center of the line

        cv2.circle(img,(x1,y1),10,(255,0,255),cv2.FILLED)
        cv2.circle(img,(x2,y2),10,(255,0,255),cv2.FILLED)
        cv2.circle(img,(cx,cy),10,(255,0,255),cv2.FILLED)  #draw a circle at center of the line
        cv2.line(img,(x1,y1),(x2,y2),(255,0,255),3)

        #finding the length b/w two points
        length = math.hypot(x2-x1,y2-y1)
        # print(length)

        vol = np.interp(length,[50,200],[minVol,maxVol])
        volBar = np.interp(length,[50,200],[400,150])
        volPer = np.interp(length,[50,250],[0,100])
        print(int(length),vol)
        volume.SetMasterVolumeLevel(vol, None)

        if length < 50:
            cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)

        cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
        cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 0), cv2.FILLED)
        cv2.putText(img,f'{int(volPer) }%',(40,450),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0))

        cv2.imshow("image", img)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
