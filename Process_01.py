import socket

# Connect to LiDAR

def connect_to_lidar(ip, port):
    """
    Establish a raw socket connection to the LiDAR sensor.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    print(f"Connected to LiDAR at {ip}:{port}")
    return sock

# Fetch raw LiDAR data
def fetch_raw_data(sock):
    """
    Fetch raw data from the LiDAR sensor via socket.
    """
    # Send a command to request data (modify as per LiDAR's protocol)
    command = b'\x02sRN LMDscandata\x03'
    sock.sendall(command)
    response = sock.recv(8192)  # Adjust the size based on LiDAR's output
    return response

# Parse raw data
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

# Process LiDAR data into segments
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

# Visualize processed data
def visualize_data(segments):
    """
    Print the processed LiDAR data for visualization.
    """
    print("Processed LiDAR Data:")
    print("Center Angle (deg) | Average Distance (m)")
    for angle, distance in segments:
        print(f"{angle:.2f}                | {distance:.2f}")

# Main function
def main():
    lidar_ip = "192.168.0.10"  # Replace with your LiDAR's IP
    lidar_port = 2112          # Replace with your LiDAR's port

    # Connect to the LiDAR
    lidar_socket = connect_to_lidar(lidar_ip, lidar_port)

    try:
        # Fetch and process data in a loop
        raw_data = fetch_raw_data(lidar_socket)
        distances = parse_raw_data(raw_data)

        # Divide data into 4-degree segments
        segments = process_data(distances, segment_size=4)

        # Visualize processed data
        visualize_data(segments)

    except KeyboardInterrupt:
        print("Terminating...")

    finally:
        lidar_socket.close()

if __name__ == "__main__":
    main()
