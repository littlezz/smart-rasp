import RPi.GPIO as GPIO
from threading import Thread
import time

led_pin = 17
sr_trigger = 18
sr_echo = 23


class RaspControler:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(led_pin, GPIO.OUT)  # LED pin set as output
        GPIO.setup(sr_trigger, GPIO.OUT)
        GPIO.setup(sr_echo, GPIO.IN)
        GPIO.add_event_detect(sr_echo, GPIO.FALLING)

    def led_on(self):
        GPIO.output(led_pin, GPIO.HIGH)

    def led_off(self):
        GPIO.output(led_pin, GPIO.LOW)

    def sr_start(self):
        GPIO.output(sr_trigger, GPIO.HIGH)
        time.sleep(1e-5)
        GPIO.output(sr_trigger, GPIO.LOW)
        print('sr start!')
        self._st = time.time()


    def sr_once(self):
        self.sr_start()
        while not GPIO.event_detect(sr_echo):
            time.sleep(0.001)
        now = time.time()
        intercept = (now - self._st)*170
        return intercept


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