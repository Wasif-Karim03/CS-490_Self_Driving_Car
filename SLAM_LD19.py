import os
import socket

def connect_to_lidar(ip, port):
    """
    Establish a raw socket connection to the LiDAR sensor.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    print(f"Connected to LiDAR at {ip}:{port}")
    return sock

def fetch_raw_data(sock):
    """
    Fetch raw data from the LiDAR sensor via socket.
    """
    # Send a command to request data (modify as per LiDAR's protocol)
    command = b'\x02sRN LMDscandata\x03'
    sock.sendall(command)
    response = sock.recv(8192)  # Adjust the size based on LiDAR's output
    return response

def parse_raw_data(raw_data):
    """
    Parse the raw LiDAR data to extract distance values.
    """
    data_str = raw_data.decode('ascii', errors='ignore')
    lines = data_str.split('\n')

    distances = []
    for line in lines:
        if 'DIST' in line:  # Replace with actual indicator in your LiDAR's protocol
            hex_values = line.split()
            for value in hex_values:
                try:
                    distance = int(value, 16) / 1000.0  # Convert hex to meters
                    distances.append(distance)
                except ValueError:
                    continue
    return distances

def process_data(distances, segment_size=4):
    """
    Divide the data into segments and calculate average distances.

    :param distances: List of distances for 360 degrees.
    :param segment_size: Size of each segment in degrees.
    :return: List of tuples containing center angle and average distance.
    """
    segments = []
    total_points = len(distances)
    points_per_segment = total_points // (360 // segment_size)

    for i in range(0, total_points, points_per_segment):
        segment_points = distances[i:i + points_per_segment]
        if segment_points:
            avg_distance = sum(segment_points) / len(segment_points)
            center_angle = (i + (points_per_segment // 2)) * (360 / total_points)
            segments.append((center_angle, avg_distance))

    return segments

def save_map(segments, file_path):
    """
    Save the processed LiDAR data to a map file.

    :param segments: Processed segments of LiDAR data.
    :param file_path: Path to save the map.
    """
    with open(file_path, 'w') as file:
        file.write("Center Angle (deg), Average Distance (m)\n")
        for angle, distance in segments:
            file.write(f"{angle:.2f}, {distance:.2f}\n")
    print(f"Map saved to {file_path}")

def load_and_visualize_map(file_path):
    """
    Load the saved map and visualize the data.

    :param file_path: Path of the saved map.
    """
    if not os.path.exists(file_path):
        print("Map file does not exist.")
        return

    print("Loaded Map Data:")
    print("Center Angle (deg) | Average Distance (m)")
    with open(file_path, 'r') as file:
        next(file)  # Skip header
        for line in file:
            angle, distance = line.strip().split(', ')
            print(f"{angle}                | {distance}")

def main():
    lidar_ip = "192.168.0.10"  
    lidar_port = 2112          
    # Connect to the LiDAR
    lidar_socket = connect_to_lidar(lidar_ip, lidar_port)

    try:
        # Fetch and process data
        raw_data = fetch_raw_data(lidar_socket)
        distances = parse_raw_data(raw_data)

        # Divide data into 4-degree segments
        segments = process_data(distances, segment_size=4)

        # Save and visualize the map
        map_file_path = "lidar_map.csv"
        save_map(segments, map_file_path)
        load_and_visualize_map(map_file_path)

    except KeyboardInterrupt:
        print("Terminating...")

    finally:
        lidar_socket.close()

if __name__ == "__main__":
    main()
