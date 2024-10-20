import RPi.GPIO as GPIO
import time
import cv2
import torch

# Set up the GPIO 
def setup_gpio(pin):
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)
        pwm = GPIO.PWM(pin, 50)
        pwm.start(7.5)  # Neutral position
        return pwm
    except Exception as e:
        print(f"Failed to initialize GPIO pin {pin}: {e}")
        GPIO.cleanup()
        return None

# Initialize YOLOv5 model
def load_model(model_path):
    model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path)
    return model

# Detect obstacles in the frame
def detect_obstacles(model, frame):
    results = model(frame)
    detections = results.xyxy[0]  # Get the detection results
    return detections

# Get the top 5 largest obstacles' coordinates
def get_largest_obstacles(detections, top_n=5):
    areas = []
    
    for *bbox, conf, cls in detections:
        x1, y1, x2, y2 = map(int, bbox)
        area = (x2 - x1) * (y2 - y1)
        areas.append((area, (x1, y1, x2, y2)))

    # Sort by area in descending order and get the top N largest
    largest_obstacles = sorted(areas, key=lambda x: x[0], reverse=True)[:top_n]
    return [coords for area, coords in largest_obstacles]

# Draw bounding boxes on the frame
def draw_boxes(frame, boxes):
    for (x1, y1, x2, y2) in boxes:
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Draw a green box
    return frame

# Move virtual joystick by percentage
def move(port, percentage):
    if 0 <= percentage <= 100:
        duty_cycle = 5 + (percentage / 100) * 5 
        port.ChangeDutyCycle(duty_cycle)
    else:
        print("Percentage out of range: Use a value between 0 and 100")
    time.sleep(.1)

# Calibrate the port
def calibrate(port):
    print("Calibrating... moving to low position.")
    move(port, 0)
    time.sleep(2)
    print("Moving to high position.")
    move(port, 100)
    time.sleep(2)
    print("Returning to neutral.")
    move(port, 50)

# Maintain stable position by adjusting throttle based on drift
def stabilize_drone(throttle_port, current_position, target_position):
    if abs(current_position - target_position) > 5:  # Adjust threshold as needed
        if current_position < target_position:
            move(throttle_port, 60)  # Move slightly forward
        else:
            move(throttle_port, 40)  # Move slightly backward
    else:
        move(throttle_port, 50)  # Stay neutral

# Clean up GPIO port
def cleanup(port):
    port.stop()
    GPIO.cleanup()

# Example usage
if __name__ == "__main__":
    model_path = 'path_to_your_model.pt'  # Change this to your model path
    model = load_model(model_path)

    # Load an image or video frame (example for image)
    frame = cv2.imread('../image.jpg')  # Change to your image path
    detections = detect_obstacles(model, frame)

    # Get the top 5 largest obstacles
    largest_obstacles = get_largest_obstacles(detections, top_n=5)

    # Draw boxes around the largest obstacles
    frame_with_boxes = draw_boxes(frame, largest_obstacles)

    # Display the result
    cv2.imshow('Detected Obstacles', frame_with_boxes)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
