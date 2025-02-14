#! /usr/bin/python3

# This python program for a Raspberry Pi emulates a pedestrian crossing traffic light system.
# Connect LEDs and an active buzzer in series with a 220R resistor on each of the GPIO pins
# shown in the Pin setup section.  Connect a button to ground on BUTTON_PIN.
# Adjust the various delays in the Delay settings section as desired.
# Run the program and press the button to change the lights!
# CTRL-C will cleanup and end the program.

import RPi.GPIO as GPIO
import time
import random

# Pin setup
RED_PIN = 17
AMBER_PIN = 27
GREEN_PIN = 22
BUTTON_PIN = 10
BEEP_PIN = 18
WALK_PIN = 15
DONTWALK_PIN = 14
WAIT_PIN = 23

# Delay settings
initial_delay = 2  # Initial short delay
max_delay = 15      # Maximum delay after rapid button presses
no_press_reset_time = 100  # Time in seconds to reset the delay if no button presses
WALK_DURATION = 10
CHANGE_DELAY = 2  # Delay between lights changing eg. AMBER light duration
BEEP_DURATION = WALK_DURATION / 2

# Setup GPIO mode
GPIO.setmode(GPIO.BCM)
GPIO.setup(RED_PIN, GPIO.OUT)
GPIO.setup(AMBER_PIN, GPIO.OUT)
GPIO.setup(GREEN_PIN, GPIO.OUT)
GPIO.setup(WALK_PIN, GPIO.OUT)
GPIO.setup(DONTWALK_PIN, GPIO.OUT)
GPIO.setup(BEEP_PIN, GPIO.OUT)
GPIO.setup(WAIT_PIN, GPIO.OUT)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

current_delay = initial_delay
last_green_time = time.time()


def beep(duration):
    while duration > 0:
        for i in range(5):
            GPIO.output(BEEP_PIN,GPIO.HIGH)
            #print("beep")
            time.sleep(0.1)
            GPIO.output(BEEP_PIN,GPIO.LOW)
            time.sleep(0.1)
        duration -= 1


def traffic_light():
    global current_delay, last_green_time

    # Green and don't walk lights on, red and amber off
    GPIO.output(DONTWALK_PIN, GPIO.HIGH)
    GPIO.output(GREEN_PIN, GPIO.HIGH)
    GPIO.output(AMBER_PIN, GPIO.LOW)
    GPIO.output(RED_PIN, GPIO.LOW)
    print("Don't Walk")

    # Wait for button press
    while GPIO.input(BUTTON_PIN) == GPIO.HIGH:
        if time.time() - last_green_time > no_press_reset_time:
            current_delay = initial_delay  # Reset delay if no button presses for a while
        time.sleep(0.1)

    # Wait light on
    GPIO.output(WAIT_PIN, GPIO.HIGH)

    # Delay before changing the lights
    print("Wait: {:.2f} seconds".format(current_delay))
    time.sleep(current_delay)

    # Introduce random delay for the next button press
    current_delay = random.uniform(current_delay, max_delay)

    # Amber light on, green off
    GPIO.output(AMBER_PIN, GPIO.HIGH)
    GPIO.output(GREEN_PIN, GPIO.LOW)
    # print("Amber light on")
    time.sleep(CHANGE_DELAY)  # Amber light duration

    # Red light on, amber off
    GPIO.output(RED_PIN, GPIO.HIGH)
    GPIO.output(AMBER_PIN, GPIO.LOW)
    # print("Red light on")
    time.sleep(CHANGE_DELAY)  # delay before allowing pedestrians to cross

    # Walk light on, Wait and Don't Walk lights off
    GPIO.output(WAIT_PIN, GPIO.LOW)
    GPIO.output(DONTWALK_PIN, GPIO.LOW)
    GPIO.output(WALK_PIN, GPIO.HIGH)
    print("Walk")

    # Beep for half of the Walk Duration
    beep(BEEP_DURATION)
    GPIO.output(WALK_PIN, GPIO.LOW)
    time.sleep(BEEP_DURATION)  # Silent for the 2nd half of walk duration

    # Don't Walk light on
    GPIO.output(DONTWALK_PIN, GPIO.HIGH)
    print("Don't Walk")
    time.sleep(CHANGE_DELAY)  # delay before returning to green

    # Return to green light
    GPIO.output(AMBER_PIN, GPIO.HIGH)
    print("Red and Amber lights on")
    time.sleep(2)  # Amber light duration
    GPIO.output(RED_PIN, GPIO.LOW)
    GPIO.output(AMBER_PIN, GPIO.LOW)
    GPIO.output(GREEN_PIN, GPIO.HIGH)
    # print("Green light on")

    last_green_time = time.time()
    if current_delay < max_delay:
        current_delay += 1  # Increment delay after each button press

try:
    while True:
        traffic_light()
except KeyboardInterrupt:
    GPIO.cleanup()
