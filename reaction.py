from gpiozero import LED, Button
from time import sleep
from random import uniform
from gpiozero import Button

led = LED(4)
led.on()
sleep(uniform(5, 10))
led.off()



left_button = Button(14)
right_button = Button(15)


def pressed(button):
	print(str(button.pin.number) + ' won the game')

right_button.when_pressed = pressed
left_button.when_pressed = pressed
