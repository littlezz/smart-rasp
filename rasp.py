import platform
if platform.system() != 'Darwin':
    import RPi.GPIO as GPIO
from threading import Thread
import time
import asyncio
from collections import deque

led_pin = 17
sr_trigger = 18
sr_echo = 23


class RaspController:
    def __init__(self):
        self._init()

    def _init(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(led_pin, GPIO.OUT)  # LED pin set as output
        GPIO.setup(sr_trigger, GPIO.OUT)
        GPIO.setup(sr_echo, GPIO.IN)
        GPIO.add_event_detect(sr_echo, GPIO.FALLING)

    def led_on(self):
        GPIO.output(led_pin, GPIO.HIGH)

    def led_off(self):
        GPIO.output(led_pin, GPIO.LOW)

    def _sr_start(self):
        GPIO.output(sr_trigger, GPIO.HIGH)
        time.sleep(1e-5)
        GPIO.output(sr_trigger, GPIO.LOW)
        self._st = time.time()

    def sr_once_block(self):
        self._sr_start()
        while not GPIO.event_detected(sr_echo):
            time.sleep(0.001)
        now = time.time()
        intercept = (now - self._st)*170
        return intercept

    @asyncio.coroutine
    def sr_once(self):
        self._sr_start()
        while not GPIO.event_detected(sr_echo):
            yield from asyncio.sleep(0.001)
        now = time.time()
        intercept = (now - self._st) * 170
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
        print('clean up!')

if platform.system() != 'Darwin':
    rcl = RaspController()
else:
    from random import random, uniform
    class DummyRCL:
        def led_on(self):
            pass

        def led_off(self):
            pass

        @asyncio.coroutine
        def sr_once(self):
            return uniform(0,0.6)

        def cleanup(self):
            pass

    rcl = DummyRCL()

def loop_sr():

    @asyncio.coroutine
    def _loop():
        while True:
            intercept = yield from rcl.sr_once()
            print(intercept)
            yield from asyncio.sleep(0.5)

    loop = asyncio.get_event_loop()
    loop.create_task(_loop())
    try:
        loop.run_forever()
    finally:
        loop.close()
        rcl.cleanup()
