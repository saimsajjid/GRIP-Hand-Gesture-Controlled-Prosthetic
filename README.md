# GRIP-Hand-Gesture-Controlled-Prosthetic



https://github.com/user-attachments/assets/dd8bfef5-d15d-412c-beaf-faa9d2564896



A gesture-controlled robotic hand using Python, OpenCV, cvzone, and Arduino.
# G.R.I.P. Hand  
**Gesture Responsive Intelligent Prosthetic Hand**

##  Project Overview
G.R.I.P. Hand is a gesture-controlled robotic hand that mimics human finger movements
using a laptop webcam, Python-based hand tracking, and servo motors controlled by Arduino.

This is my first self-built hardware + software project, developed through hands-on learning,
experimentation, and real-world debugging.

---

## ⚙️ How It Works
1. A laptop webcam captures real-time hand gestures
2. Python uses OpenCV and cvzone to detect finger states (open / closed)
3. Each finger is converted into binary data (1 or 0)
4. This data is sent via Serial Communication to Arduino
5. Arduino controls servo motors to replicate the same finger pattern

Example:
10101 → Thumb, Middle, Pinky open

---

## 🧩 Technologies Used
- Python 3.12
- OpenCV 4.12.0.88
- cvzone 1.6.1
- NumPy 1.26.4
- PySerial 3.5
- Arduino (C/C++)
- Servo Motors (MG90S)

---


---

## Softwares Used
- Pycharm
- Arduino IDE

---

## 🔌 Hardware Components
- Arduino Uno
- 5 × Servo Motors
- External 5V Power Supply
- Jumper Wires
- 3D Printed Hand Frame

---

## 📌 Applications
- Prosthetic and assistive devices
- Human–machine interaction
- Robotics and automation
- Gesture-based control systems
- Educational demonstrations

---

## 🧪 Project Status
✅ Gesture detection working  
✅ Arduino communication working  

---

##  Acknowledgment
This project was built as a learning experience.
