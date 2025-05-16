# HandGestureVolumeControl
Hand Gesture Controlled Volume System using OpenCV, MediaPipe, and Pycaw for real-time volume adjustment with webcam input

## ✨ Features

- Real-time hand tracking using MediaPipe.
- Control system volume by changing the distance between your thumb and index finger.
- Visual feedback: volume bar and percentage display.
- Green dot indicator when fingers are close (mute position).

## 📁 Project Structure

┣ 📜 main.py # Main script that runs the volume control
┣ 📜 HandTrackingModule.py # Custom module for hand detection and landmark tracking
┗ 📜 README.md # Project documentation

## 🛠️ Requirements

- Python 3.x
- OpenCV (`opencv-python`)
- MediaPipe
- NumPy
- Pycaw
- comtypes

You can install the required libraries using pip:

pip install opencv-python mediapipe numpy pycaw comtypes

🚀 How to Run

1.Clone the repository:
git clone https://github.com/your-username/HandGestureVolumeControl.git
cd HandGestureVolumeControl

2.Run the main script:
python main.py
3.Make a "pinching" gesture with your thumb and index finger. Moving them closer decreases the volume, and moving them apart increases it.
4.Press q to exit the program.

🧠 How It Works

HandTrackingModule.py uses MediaPipe to detect hand landmarks in a webcam frame.
In main.py, the distance between landmarks 4 (thumb tip) and 8 (index finger tip) is calculated using the Euclidean distance formula.
This distance is mapped to a volume level using NumPy’s interp() function.
Volume is controlled using Pycaw, which provides an interface to the Windows Core Audio API.

Enjoy touch-free volume control! 🔊🖐️
