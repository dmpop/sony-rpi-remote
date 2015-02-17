#!/usr/bin/python
from bottle import post, route, request, run
import os, time

from time import sleep
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

def release():
    GPIO.setup(23, GPIO.OUT)
    GPIO.setup(25, GPIO.OUT)
    GPIO.output(23, True)
    time.sleep(0.5)
    GPIO.output(25, True)
    time.sleep(0.5)
    GPIO.output(25, False)
    GPIO.output(23, False)

@route('/')
@route('/', method='POST')
def release_control():
    if (request.POST.get("shutter_release")):
        release()
    if (request.POST.get("number")):
        i = 1
        number = int(request.forms.get('number'))
        interval = int(request.forms.get('interval'))
        while (i <= number):
            release()
            time.sleep(interval)
            i = i + 1
    if (request.POST.get("shutdown")):
        os.system("sudo halt")
    return """
    <title>SONY Raspberry Pi Remote</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <form method="POST" action="/">
    <div id="content"><p><input id="btn" name="shutter_release" type="submit" value="Shutter Release"></p>
    <p>Photos: <input name="number" type="text" size="3"/> Interval: <input name="interval" type="text" size="3"/> sec.</p>
    <p><input id="btn" value="Start" type="submit" /></p>
    <p><input id="btn" class="warning" name="shutdown" value="Shutdown" type="submit" /></p>
    </form></div>
    <style>
        body {
        font: 15px/25px 'Open Sans', sans-serif;
        }
        #content {
        margin: 0px auto;
        text-align: center;
        }
        #btn {
        width: 11em;  height: 2em;
        background: rgb(66, 184, 221);
        border-radius: 5px;
        color: #fff;
        font-family: 'Fira Sans', sans-serif;
        font-size: 25px;
        font-weight: 900;
        text-shadow: 0 1px 1px rgba(0, 0, 0, 0.2);
        letter-spacing: 3px;
        border:none;
        }
        #btn.warning {
        background: rgb(223, 117, 20);
        }
    </style>
    """
run(host="0.0.0.0",port=8080)
