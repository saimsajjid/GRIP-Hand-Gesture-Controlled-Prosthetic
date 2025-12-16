/*
 * ======================================================================================
 * !!! MUST READ BEFORE UPLOADING !!!
 * ======================================================================================
 * NEW USER GUIDE - DO NOT SKIP:
 * * 1. PIN CONNECTIONS (Lines 34-38): 
 * Make sure your physical wiring matches these Digital PWM pins.
 * * 2. SERVO CALIBRATION (Lines 93-125):
 * Go to these lines to set your start/end angles. 
 * - 180 might be "Open" for me, but "Closed" or "Broken" for your hand.
 * - Test limits slowly!
 * * 3. BINARY LOGIC:
 * The code expects a string like "$10101".
 * 1 = Active/Open (usually)
 * 0 = Inactive/Closed (usually)
 * ======================================================================================
 */

#include <Servo.h>

// ==========================================
// CONFIGURATION
// ==========================================
#define numOfValsRec 5
#define digitsPerValRec 1

// Servo Objects
Servo servoThumb;
Servo servoIndex;
Servo servoMiddle;
Servo servoRing;
Servo servoPinky;

// Data Handling
int valsRec[numOfValsRec];
int stringLength = numOfValsRec * digitsPerValRec + 1; // Expecting "$00000"
int counter = 0;
bool counterStart = false;
String receivedString;

void setup() {
  Serial.begin(9600);
  
  // ---------------------------------------------------------
  // PIN ASSIGNMENTS (Check your wiring!)
  // ---------------------------------------------------------
  servoThumb.attach(6);
  servoIndex.attach(4);
  servoMiddle.attach(5);
  servoRing.attach(2);
  servoPinky.attach(3);
}

void receiveData() {
  while (Serial.available()) {
    char c = Serial.read();

    if (c == '$') {
      counterStart = true;
    }

    if (counterStart) {
      if (counter < stringLength) {
        receivedString = String(receivedString + c);
        counter++;
      }

      if (counter >= stringLength) {
        // Parse "$00000" into integers
        for (int i = 0; i < numOfValsRec; i++) {
          int num = (i * digitsPerValRec) + 1;
          valsRec[i] = receivedString.substring(num, num + digitsPerValRec).toInt();
        }
        receivedString = "";
        counter = 0;
        counterStart = false;
      }
    }
  }
}

void loop() {
  receiveData();

  // =================================================================================
  //  CALIBRATION ZONE (Lines 93-125)
  //  Adjust the values inside .write() to fit your mechanical limits.
  // =================================================================================

  // --- THUMB (valsRec[0]) ---
  // If Python sends 1 ($1xxxx), Thumb moves to 180.
  if (valsRec[0] == 1) { 
    servoThumb.write(180); // SET OPEN ANGLE HERE
  } else { 
    servoThumb.write(0);   // SET CLOSED ANGLE HERE
  }

  // --- INDEX FINGER (valsRec[1]) ---
  // If Python sends 0 ($x0xxx), Index moves to 140. (Note inverted logic here)
  if (valsRec[1] == 0) { 
    servoIndex.write(140); // SET ACTION ANGLE HERE
  } else { 
    servoIndex.write(0);   // SET REST ANGLE HERE
  }

  // --- MIDDLE FINGER (valsRec[2]) ---
  if (valsRec[2] == 1) { 
    servoMiddle.write(180); // SET OPEN ANGLE HERE
  } else { 
    servoMiddle.write(0);   // SET CLOSED ANGLE HERE
  }

  // --- RING FINGER (valsRec[3]) ---
  if (valsRec[3] == 1) { 
    servoRing.write(180); // SET OPEN ANGLE HERE
  } else { 
    // Example: 70 degrees might be the mechanical limit for your ring finger
    servoRing.write(70);  // SET CLOSED ANGLE HERE
  }

  // --- PINKY FINGER (valsRec[4]) ---
  if (valsRec[4] == 1) { 
    servoPinky.write(180); // SET OPEN ANGLE HERE
  } else { 
    servoPinky.write(0);   // SET CLOSED ANGLE HERE
  }
}
