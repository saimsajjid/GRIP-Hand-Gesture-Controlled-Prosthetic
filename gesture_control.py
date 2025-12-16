"""
=======================================================================================
!!! CRITICAL: READ THIS BEFORE RUNNING !!!
=======================================================================================
1. DEPENDENCIES & VERSIONS:
   This project is extremely sensitive to library versions (especially MediaPipe/CVZone).
   -> PLEASE READ THE 'README.md' FILE FOR EXACT VERSION NUMBERS.
   -> If you install the wrong versions, the hand tracking will crash or not open.

2. HARDWARE SETUP:
   -> CHECK YOUR COM PORT: This code uses 'COM5'. Your Arduino is likely on a different 
      port (e.g., COM3, /dev/ttyUSB0). Change line 32 to match your system.

3. CAMERA SETUP:
   -> If the window opens but remains BLACK or crashes immediately:
      Change 'cv2.VideoCapture(0)' to 'cv2.VideoCapture(1)' (Line 59).
      0 = Default Internal Camera
      1 = External USB Webcam
   
4. HOW IT WORKS:
   -> Detects hand gestures via Webcam.
   -> Converts fingers to binary string (e.g., "$10101").
   -> Sends data to Arduino via Serial.
=======================================================================================
"""

import cv2
from cvzone.HandTrackingModule import HandDetector
import serial
import time

# ==========================================
# CONFIGURATION
# ==========================================
# CHANGE THIS to your Arduino's actual port!
# Windows: "COM3", "COM5", etc. | Mac/Linux: "/dev/tty..."
SERIAL_PORT = 'COM5' 
BAUD_RATE = 9600

# ==========================================
# ARDUINO SERIAL CONNECTION
# ==========================================
arduino = None
try:
    print(f"Attempting to connect to {SERIAL_PORT}...")
    arduino = serial.Serial(SERIAL_PORT, BAUD_RATE)
    time.sleep(2)  # Critical: Arduino resets on serial connection. Wait for it.
    print(f"SUCCESS: Connected to Arduino on {SERIAL_PORT}")
except Exception as e:
    print(f"\n[ERROR] Could not connect to Arduino on {SERIAL_PORT}.")
    print("-> Check your cable.")
    print("-> Check if another program (like Arduino IDE) is using the port.")
    print("-> Running in 'No-Arduino' mode (Visuals only).\n")
    arduino = None

# ==========================================
# HAND DETECTOR SETUP
# ==========================================
# detectionCon=0.8 reduces false positives (jittery fingers)
detector = HandDetector(maxHands=1, detectionCon=0.7)

# ==========================================
# CAMERA SETUP
# ==========================================
# 0 = Default Laptop Camera
# 1 = External USB Webcam
# If code crashes or screen is black, change this number!
cap = cv2.VideoCapture(0) 

cap.set(3, 1280)  # Width
cap.set(4, 720)   # Height

prev_data = ""

print("Starting video stream... Press 'q' to exit.")

while True:
    success, img = cap.read()
    if not success:
        print("[ERROR] Camera not detected or frame could not be read.")
        print("-> Hint: Try changing cv2.VideoCapture(0) to 1 or 2.")
        break

    # 1. Find Hand Landmarks
    hands, img = detector.findHands(img)  
    
    # Default string if no hand is detected
    data_to_send = "$00000"  

    if hands:
        # Get the first hand detected
        hand = hands[0]
        
        # 2. Check which fingers are up
        # Returns list like [1, 0, 1, 1, 1] (Thumb, Index, Middle, Ring, Pinky)
        fingers = detector.fingersUp(hand)
        
        # 3. Format Data for Arduino
        # Join list into string: "10111"
        data_str = ''.join(map(str, fingers))  
        data_to_send = f"${data_str}"

        # 4. Send Data (Only if it changed to prevent Serial flooding)
        if data_str != prev_data:
            prev_data = data_str
            
            if arduino:
                try:
                    arduino.write(data_to_send.encode())
                    print(f"Sent: {data_to_send}")
                except Exception as e:
                    print(f"[Serial Error] {e}")

        # Display values on screen for debugging
        cv2.putText(img, f"Signal: {data_to_send}", (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Show the frame
    cv2.imshow("G.R.I.P Hand Control", img)

    # Exit Logic
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ==========================================
# CLEANUP
# ==========================================
cap.release()
cv2.destroyAllWindows()
if arduino:
    arduino.close()
    print("Serial connection closed.")
