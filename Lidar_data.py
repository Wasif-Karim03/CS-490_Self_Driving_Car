import socket
import struct
import time

def connect_to_lidar(ip, port):
    """
    Connect to a 360-degree LiDAR using raw socket.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    print(f"Connected to LiDAR at {ip}:{port}")
    return sock

def fetch_raw_data(sock):
    """
    Fetch raw LiDAR data over the socket.
    """
    # Example command to request data, modify based on LiDAR documentation
    command = b'\x02sRN LMDscandata\x03'
    sock.sendall(command)
    response = sock.recv(8192)  # Adjust based on expected response size
    return response

def parse_lidar_data(raw_data):
    """
    Parse raw LiDAR data into angle-distance pairs.
    """
    # Decode and split the raw response
    data_str = raw_data.decode('ascii', errors='ignore')
    lines = data_str.split('\n')
    distances = []

    for line in lines:
        if 'DIST' in line:  # Example: Look for distance data
            hex_values = line.split()
            for value in hex_values:
                try:
                    distance = int(value, 16) / 1000.0  # Convert hex to meters
                    distances.append(distance)
                except ValueError:
                    continue

    return distances

def build_laserscan_message(distances, angle_min=0.0, angle_max=360.0):
    """
    Manually construct a LaserScan-like data format.
    """
    angle_increment = (angle_max - angle_min) / len(distances)
    laserscan = {
        "angle_min": angle_min,
        "angle_max": angle_max,
        "angle_increment": angle_increment,
        "ranges": distances
    }
    return laserscan

def visualize_lidar_data(laserscan):
    """
    Simulate visualization by printing data (or save to a file for analysis).
    """
    print("LaserScan Data:")
    print(f"Angle Min: {laserscan['angle_min']} degrees")
    print(f"Angle Max: {laserscan['angle_max']} degrees")
    print(f"Angle Increment: {laserscan['angle_increment']} degrees")
    print("Ranges:")
    for i, distance in enumerate(laserscan["ranges"]):
        print(f"Angle: {i * laserscan['angle_increment']:.2f} degrees, Distance: {distance:.2f} m")

def main():
    lidar_ip = "192.168.0.10"  # Replace with your LiDAR's IP
    lidar_port = 2112          # Replace with your LiDAR's port

    # Connect to the LiDAR
    lidar_socket = connect_to_lidar(lidar_ip, lidar_port)

    try:
        while True:
            # Fetch and parse raw data
            raw_data = fetch_raw_data(lidar_socket)
            distances = parse_lidar_data(raw_data)

            # Build a LaserScan-like message
            laserscan = build_laserscan_message(distances)

            # Visualize data (or send to RViz2 using custom serialization)
            visualize_lidar_data(laserscan)

            time.sleep(1)  # Simulate periodic updates
    except KeyboardInterrupt:
        print("Terminating...")
    finally:
        lidar_socket.close()

if __name__ == "__main__":
    main()
