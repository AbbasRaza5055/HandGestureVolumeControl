# Import required libraries
import cv2  # OpenCV for image processing
import mediapipe as mp  # MediaPipe for hand tracking

# Class to detect hands and their landmarks
class handDetector:
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        # Initialize parameters
        self.mode = mode  # Static or video mode
        self.maxHands = maxHands  # Maximum number of hands to detect
        self.detectionCon = detectionCon  # Detection confidence threshold
        self.trackCon = trackCon  # Tracking confidence threshold

        # Initialize MediaPipe hands model
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.maxHands,
            min_detection_confidence=self.detectionCon,
            min_tracking_confidence=self.trackCon
        )
        self.mpDraw = mp.solutions.drawing_utils  # For drawing landmarks

    # Function to detect hands and draw landmarks
    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
        self.results = self.hands.process(imgRGB)  # Process the frame

        # If hands are detected
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                # Draw landmarks if draw=True
                if draw:
                    self.mpDraw.draw_landmarks(
                        img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img  # Return image with (or without) drawings

    # Function to extract positions of all hand landmarks
    def findPosition(self, img, handNo=0, draw=True):
        lmList = []  # List to store landmark coordinates

        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]  # Select one hand

            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape  # Get image dimensions
                cx, cy = int(lm.x * w), int(lm.y * h)  # Convert normalized coords
                lmList.append([id, cx, cy])  # Store landmark data
        return lmList  # Return list of landmarks

# Test function to visualize hand detection standalone
def main():
    cap = cv2.VideoCapture(0)  # Open webcam
    detector = handDetector()  # Create detector object

    while True:
        success, img = cap.read()  # Read frame
        img = detector.findHands(img)  # Detect hands
        lmList = detector.findPosition(img)  # Get landmark positions

        if len(lmList) != 0:
            print(lmList[4])  # Print position of thumb tip

        cv2.imshow("Image", img)  # Show result
        cv2.waitKey(1)  # Wait for key press

# Run test if this file is executed directly
if __name__ == "__main__":
    main()
