from pymavlink import mavutil

def connect_pixhawk(port='/dev/ttyUSB0', baud=115200):
    """
    Establish connection with Pixhawk.
    :param port: Serial port for Pixhawk (e.g., /dev/ttyUSB0 on Linux).
    :param baud: Baud rate for the serial connection.
    :return: MAVLink connection object.
    """
    print("Connecting to Pixhawk...")
    connection = mavutil.mavlink_connection(port, baud)
    connection.wait_heartbeat()  # Wait for the Pixhawk to send a heartbeat
    print("Connected to Pixhawk.")
    return connection

def clear_waypoints(connection):
    """
    Clear all existing waypoints from Pixhawk.
    :param connection: MAVLink connection object.
    """
    print("Clearing existing waypoints...")
    connection.mav.mission_clear_all_send(connection.target_system, connection.target_component)
    print("All waypoints cleared.")

def create_waypoint(lat, lon, alt, seq):
    """
    Create a MAVLink mission item (waypoint).
    :param lat: Latitude of the waypoint.
    :param lon: Longitude of the waypoint.
    :param alt: Altitude of the waypoint in meters.
    :param seq: Sequence number of the waypoint.
    :return: MAVLink mission item object.
    """
    return mavutil.mavlink.MAVLink_mission_item_message(
        target_system=0,                   # Target system (Pixhawk)
        target_component=0,                # Target component
        seq=seq,                           # Sequence number
        frame=mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,  # Use relative altitude
        command=mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,         # Command for waypoint navigation
        current=0,                         # Current waypoint (0 for non-current)
        autocontinue=1,                    # Autocontinue to the next waypoint
        param1=0, param2=0, param3=0, param4=0,  # Unused parameters
        x=lat,                             # Latitude
        y=lon,                             # Longitude
        z=alt                              # Altitude
    )

def upload_waypoints(connection, waypoints):
    """
    Upload a list of waypoints to the Pixhawk.
    :param connection: MAVLink connection object.
    :param waypoints: List of waypoints in (latitude, longitude, altitude) format.
    """
    print("Uploading waypoints...")
    
    # Send the mission count
    connection.mav.mission_count_send(connection.target_system, connection.target_component, len(waypoints))
    
    for seq, waypoint in enumerate(waypoints):
        lat, lon, alt = waypoint
        mission_item = create_waypoint(lat, lon, alt, seq)
        connection.mav.send(mission_item)  # Send each waypoint to Pixhawk
        print(f"Uploaded waypoint {seq + 1}: Lat={lat}, Lon={lon}, Alt={alt}")

    print("All waypoints uploaded successfully.")

def main():
    # Define the Pixhawk connection
    pixhawk_connection = connect_pixhawk(port='/dev/ttyUSB0', baud=115200)

    # Clear existing waypoints
    clear_waypoints(pixhawk_connection)

    # Define the waypoints: List of (latitude, longitude, altitude)
    waypoints = [
        (37.7749, -122.4194, 10),  # Example: San Francisco
        (37.7750, -122.4185, 15),  # Example: Nearby point
        (37.7760, -122.4170, 20)   # Example: Another point
    ]

    # Upload the waypoints
    upload_waypoints(pixhawk_connection, waypoints)

if __name__ == "__main__":
    main()
