import RPi.GPIO as GPIO

import time

GPIO.setmode(GPIO.BOARD)

GPIO.setup(40, GPIO.OUT)

GPIO.setup(38, GPIO.IN)

while 1:
	if GPIO.input(38):
#		print("Movement detected")
		GPIO.output(40, GPIO.HIGH)
	else:
#		print("No movement")
		GPIO.output(40, GPIO.LOW)

#	time.sleep(0.5)

GPIO.cleanup()


