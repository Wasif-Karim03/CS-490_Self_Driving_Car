from pymavlink import mavutil

def connect_pixhawk(port='/dev/ttyTHS1', baud=57600):
    """
    Establish connection with Pixhawk from Jetson Nano.
    :param port: UART port used for connection (e.g., /dev/ttyTHS1 on Jetson Nano).
    :param baud: Baud rate for the serial connection.
    :return: MAVLink connection object.
    """
    print("Connecting to Pixhawk...")
    connection = mavutil.mavlink_connection(port, baud)
    connection.wait_heartbeat()  # Wait for heartbeat to confirm connection
    print("Connected to Pixhawk.")
    return connection

def set_auto_mode(connection):
    """
    Set Pixhawk flight mode to AUTO for mission execution.
    :param connection: MAVLink connection object.
    """
    print("Setting flight mode to AUTO...")
    # Get mode mapping and find the mode ID for "AUTO"
    mode = 'AUTO'
    if mode not in connection.mode_mapping():
        print(f"Mode {mode} is not available on this Pixhawk.")
        return
    mode_id = connection.mode_mapping()[mode]

    # Send command to change mode
    connection.mav.set_mode_send(
        connection.target_system,
        mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
        mode_id
    )
    print(f"Flight mode set to {mode}. Awaiting confirmation...")

    # Wait for acknowledgment
    while True:
        ack_msg = connection.recv_match(type='COMMAND_ACK', blocking=True)
        if ack_msg and ack_msg.command == mavutil.mavlink.MAV_CMD_DO_SET_MODE:
            print("Flight mode AUTO confirmed.")
            break

def arm_vehicle(connection):
    """
    Arm the Pixhawk for mission start.
    :param connection: MAVLink connection object.
    """
    print("Arming vehicle...")
    connection.mav.command_long_send(
        connection.target_system,
        connection.target_component,
        mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
        0,
        1, 0, 0, 0, 0, 0, 0  # 1 to arm, 0 to disarm
    )

    # Wait for acknowledgment
    ack_msg = connection.recv_match(type='COMMAND_ACK', blocking=True)
    if ack_msg and ack_msg.command == mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM:
        print("Vehicle armed.")

def start_mission(connection):
    """
    Start the mission execution on Pixhawk.
    :param connection: MAVLink connection object.
    """
    print("Starting mission...")
    connection.mav.command_long_send(
        connection.target_system,
        connection.target_component,
        mavutil.mavlink.MAV_CMD_MISSION_START,
        0,
        0, 0, 0, 0, 0, 0, 0
    )

    # Wait for acknowledgment
    ack_msg = connection.recv_match(type='COMMAND_ACK', blocking=True)
    if ack_msg and ack_msg.command == mavutil.mavlink.MAV_CMD_MISSION_START:
        print("Mission started successfully.")

def main():
    # Connect to Pixhawk via UART (adjust port and baud for your setup)
    pixhawk_connection = connect_pixhawk(port='/dev/ttyTHS1', baud=57600)

    # Set flight mode to AUTO
    set_auto_mode(pixhawk_connection)

    # Arm the vehicle
    arm_vehicle(pixhawk_connection)

    # Start the mission
    start_mission(pixhawk_connection)

if __name__ == "__main__":
    main()
