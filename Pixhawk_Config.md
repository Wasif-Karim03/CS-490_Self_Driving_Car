#!/bin/bash

# -------------------------------
# Pixhawk Setup Script via Terminal
# -------------------------------

# Set the serial port and baud rate (Adjust as needed)
SERIAL_PORT="/dev/ttyUSB0" # Replace with your Pixhawk's serial port
BAUD_RATE=57600

# -------------------------------
# Step 1: Connect to Pixhawk
# -------------------------------
echo "Connecting to Pixhawk on $SERIAL_PORT with baud rate $BAUD_RATE"
mavproxy.py --master=$SERIAL_PORT --baudrate $BAUD_RATE --aircraft MyRover &
MAVPROXY_PID=$!
sleep 5

# -------------------------------
# Step 2: Set Frame and Mode Parameters
# -------------------------------
echo "Setting Frame and Mode Parameters"
echo "param set FRAME_CLASS 1" | mavproxy.py
sleep 2
echo "param set FRAME_TYPE 0" | mavproxy.py
sleep 2
echo "param set SERVO1_FUNCTION 73" | mavproxy.py
sleep 2
echo "param set SERVO3_FUNCTION 26" | mavproxy.py
sleep 2

# -------------------------------
# Step 3: Calibrate RC Input
# -------------------------------
echo "Calibrating RC Input"
echo "rc calibration" | mavproxy.py
sleep 5

# -------------------------------
# Step 4: Calibrate Compass and Accelerometer
# -------------------------------
echo "Calibrating Compass"
echo "module load calibrate" | mavproxy.py
sleep 2
echo "calibrate compass" | mavproxy.py
sleep 5

echo "Calibrating Accelerometer"
echo "calibrate accel" | mavproxy.py
sleep 5

# -------------------------------
# Step 5: Set Up GPS
# -------------------------------
echo "Checking GPS Status"
echo "gps" | mavproxy.py
sleep 2

# -------------------------------
# Step 6: Set Control Modes
# -------------------------------
echo "Setting Manual Mode"
echo "mode MANUAL" | mavproxy.py
sleep 2

echo "Setting Auto Mode"
echo "mode AUTO" | mavproxy.py
sleep 2

# -------------------------------
# Step 7: Upload Waypoints
# -------------------------------
echo "Uploading Waypoints"
echo "wp load mission.txt" | mavproxy.py
sleep 2

echo "Listing Waypoints"
echo "wp list" | mavproxy.py
sleep 2

# -------------------------------
# Step 8: Monitor Status
# -------------------------------
echo "Monitoring Vehicle Status"
echo "status" | mavproxy.py
sleep 5

# -------------------------------
# Cleanup
# -------------------------------
echo "Closing MAVProxy session"
kill $MAVPROXY_PID
