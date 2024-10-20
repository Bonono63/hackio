import RPi.GPIO as GPIO
import time
import cv2

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


# Get the largest obstacle's coordinates
def get_largest_obstacle(detections):
    largest_area = 0
    largest_obstacle = None

    for *bbox, conf, cls in detections:
        x1, y1, x2, y2 = map(int, bbox)
        area = (x2 - x1) * (y2 - y1)
        if area > largest_area:
            largest_area = area
            largest_obstacle = (x1, y1, x2, y2)

    return largest_obstacle

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