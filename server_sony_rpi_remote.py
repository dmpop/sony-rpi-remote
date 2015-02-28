#!/usr/bin/python

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from bottle import post, route, request, run
import os, time

from time import sleep
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
#Turn the LED on pin 27 on (indicates that the server is up and running)
GPIO.setup(27, GPIO.OUT)
GPIO.output(27, True)

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
    if (request.POST.get("start")):
        i = 1
        number = int(request.forms.get('number'))
        interval = int(request.forms.get('interval'))
        while (i <= number):
            release()
            time.sleep(interval)
            i = i + 1
    if (request.POST.get("stop")):
            GPIO.output(27, False)
            os.system("killall -KILL python")
    if (request.POST.get("shutdown")):
            os.system("sudo halt")
    return """
    <title>Sony Raspberry Pi Remote</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <form method="POST" action="/">
    <div id="content"><p><input id="btn" name="shutter_release" type="submit" value="Shutter Release"></p>
    <p class=right">Photos: <input name="number" type="text" size="3"/> Interval: <input name="interval" type="text" size="3"/> sec.</p>
    <p><input id="btn" name="start" value="Start" type="submit" /></p>
    <p><input id="btn" class="orange" name="stop" value="Stop" type="submit" /></p>
    <p><input id="btn" class="red" name="shutdown" value="Shut down" type="submit" /></p>
    </form>
    <p class="left">Press <strong>Shutter Release</strong> for a single shot.</p>
    <p class="left">Use the appropriate fields to specify the number of photos and the interval between them in seconds, then press <strong>Start</strong>.</p>
    <p class="left">Press <strong>Stop</strong> to terminate the app.</p>
    <p class="left">Press <strong>Shutdown</strong> to shut down Raspberry Pi.</p>
    </div>
    <style>
    <link href='http://fonts.googleapis.com/css?family=Open+Sans:400,600,700' rel='stylesheet' type='text/css'>
    body {
        font: 15px/25px 'Open Sans', sans-serif;
    }
    p.left {
        text-align: left;
    }
    p.right {
        text-align: right;
    }
    #content {
        font: 15px/25px 'Open Sans', sans-serif;
        margin: 0px auto;
        width: 275px;
        text-align: left;
    }
    #btn {
        width: 11em;  height: 2em;
        background: #3399ff;
        border-radius: 5px;
        color: #fff;
        font-family: 'Open Sans', sans-serif; font-size: 25px; font-weight: 900;
        letter-spacing: 3px;
        border:none;
    }
    #btn.orange {
        background: #ff9900;
    }
    #btn.red {
        background: #cc0000;
    }
    </style>
    """
run(host="0.0.0.0",port=8080, debug=True, reloader=True)
