This python program for a Raspberry Pi emulates a pedestrian crossing traffic light system, using LEDs, a button and a buzzer connected to GPIO pins.

Connect LEDs and an active buzzer in series with a 220R resistor on each of the GPIO pins
shown in the Pin setup section.  Connect a button to ground on BUTTON_PIN.

Default GPIO Pin settings are:
* RED_PIN = 17
* AMBER_PIN = 27
* GREEN_PIN = 22
* BUTTON_PIN = 10
* BEEP_PIN = 18
* WALK_PIN = 15
* DONTWALK_PIN = 14
* WAIT_PIN = 23

Adjust the various delays in the Delay settings section as desired.

Run the program and press the button to change the lights!

CTRL-C will cleanup and end the program.
