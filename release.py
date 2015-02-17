#!/usr/bin/env python
from time import sleep
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(25, GPIO.OUT)
GPIO.output(23, True)
sleep(0.5)
GPIO.output(25, True)
sleep(0.5)
GPIO.output(25, False)
GPIO.output(23, False)
