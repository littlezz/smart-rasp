import RPi.GPIO as GPIO
from threading import Thread

led_pin = 17
sr_trigger = 18
sr_echo = 23


class RaspControler:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(led_pin, GPIO.OUT)  # LED pin set as output
        GPIO.setup(sr_trigger, GPIO.OUT)
        GPIO.setup(sr_echo, GPIO.IN)
        self.pwm = GPIO.PWM(sr_trigger, 10)

    def led_on(self):
        GPIO.output(led_pin, GPIO.HIGH)

    def led_off(self):
        GPIO.output(led_pin, GPIO.LOW)

    def sr_start(self):
        self.pwm.start(1)
        print('sr start!')

    def debug_output(self):
        def output():
            import time
            while True:
                print(GPIO.input(sr_echo))
                time.sleep(0.001)

        self.t = Thread(target=output)
        self.t.start()

    def cleanup(self):
        GPIO.cleanup()


rasp = RaspControler()