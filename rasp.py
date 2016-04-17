import RPi.GPIO as GPIO

led_pin = 13

class RaspControler:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(led_pin, GPIO.OUT)  # LED pin set as output

    def led_on(self):
        GPIO.output(led_pin, GPIO.HIGH)

    def led_off(self):
        GPIO.output(led_pin, GPIO.LOW)


rasp = RaspControler()