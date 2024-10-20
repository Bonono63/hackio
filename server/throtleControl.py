import RPi.GPIO as GPIO
import time
import keyboard

# Set up the GPIO 
def setup_gpio(pin):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    pwm = GPIO.PWM(pin, 50)
    pwm.start(7.5) 
    return pwm

# Move virtual joystick
def move(pwm, position):
    if position == "high":
        pwm.ChangeDutyCycle(10)
    elif position == "low":
        pwm.ChangeDutyCycle(5)
    else:
        print("Unknown position: Use 'high' or 'low'")
    time.sleep(1) 

def cleanup(pwm):
    pwm.stop()
    GPIO.cleanup()

pin = setup_gpio(17)

while True:
    if keyboard.is_pressed('q'):
        break
    if keyboard.is_pressed('w'):
        move(pin, high)
    if keyboard.is_pressed('s'):
        move(pin, low)

cleanup(pin)

