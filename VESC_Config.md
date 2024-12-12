# install VESC Software
sudo apt install vesc-tool-cli

# Connect VESC
ls /dev/tty*  # Look for the port (e.g., /dev/ttyUSB0)
vesc_tool_cli --port /dev/ttyUSB0

# Motor Config
vesc_tool_cli --set-motor-config

# Input Setup 
vesc_tool_cli --set-input-config

# Read Setting 
vesc_tool_cli --get-config

# Write Setting 
vesc_tool_cli --write-config

# Open VESC Terminal
screen /dev/ttyUSB0 115200
set_duty 0.5  # Set throttle - 50% throttle 
set_rpm 3000  #Set RPM
set_current 10  # Set Current - 10A
 

# Check Motor Status 
vesc_tool_cli --monitor


# Basic Script to congig  (These values can varry based on car and it's setup)
# !/bin/bash

VESC_PORT="/dev/ttyUSB0"
echo "Connecting to VESC on $VESC_PORT"
vesc_tool_cli --port $VESC_PORT --set-motor-config <<EOF
max_current=60
min_current=-60
max_voltage=50
min_voltage=10
pole_count=14
EOF
vesc_tool_cli --port $VESC_PORT --set-input-config <<EOF
input_mode=PPM
EOF

# Save the configuration
vesc_tool_cli --port $VESC_PORT --write-config
echo "Configuration complete."
