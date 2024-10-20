import RPi.GPIO as GPIO
import time

# Set up GPIO PIN
signal_pin = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(signal_pin,GPIO.OUT)

# Set up pulse width modulation
pwm = GPIO.PWM(signal_pin, 50)
pwm.start(7.5)

try:
    while True:
        pwm.ChangeDutyCycle(5)
        time.sleep(1)
        pwm.ChangeDutyCycle(10)
        time.sleep(1)
except KeyboardInterrupt:
    pass

# Clean up
pwm.stop()
GPIO.cleanup()
