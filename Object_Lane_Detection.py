import cv2
import numpy as np
from ultralytics import YOLO

model = YOLO('yolov8n.pt')

mode = input("Select mode: 'video' to play video file or 'camera' for live feed: ")

if mode == 'video':
    video_path = input("Enter the video file path: ")
    cap = cv2.VideoCapture(video_path)
elif mode == 'camera':
    cap = cv2.VideoCapture(0)
else:
    print("Invalid mode selected. Exiting...")
    exit()

if not cap.isOpened():
    print("Error: Could not open video stream or file.")
    exit()

def detect_lanes(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, 50, 150)
    
    height, width = frame.shape[:2]
    mask = np.zeros_like(edges)
    polygon = np.array([[
        (0, height), (width, height), (width, height // 2), (0, height // 2)
    ]], np.int32)
    cv2.fillPoly(mask, polygon, 255)
    masked_edges = cv2.bitwise_and(edges, mask)
    
    lines = cv2.HoughLinesP(masked_edges, 1, np.pi/180, threshold=100, minLineLength=40, maxLineGap=5)
    
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)
    
    return frame

def process_detection_results(results, frame):
    class_names = model.names
    
    for result in results:
        boxes = result.boxes.xyxy
        confs = result.boxes.conf
        labels = result.boxes.cls
        
        for i in range(len(boxes)):
            x1, y1, x2, y2 = map(int, boxes[i])
            label = int(labels[i])
            confidence = confs[i]
            
            class_name = class_names[label]
            
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
            cv2.putText(frame, f'{class_name} {confidence:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
            
            if class_name == 'person':
                print("Warning: Pedestrian detected! Slowing down...")
            elif class_name == 'car':
                print("Car detected ahead, adjusting speed...")
            elif class_name == 'traffic light':
                print("Traffic light detected!")
    return frame

while True:
    ret, frame = cap.read()
    
    if not ret:
        print("Failed to grab frame or end of video file.")
        break

    results = model(frame)

    frame_with_detections = process_detection_results(results, frame.copy())

    frame_with_lanes = detect_lanes(frame_with_detections)
    
    cv2.imshow('Self-Driving Car - YOLOv8 and Lane Detection', frame_with_lanes)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()