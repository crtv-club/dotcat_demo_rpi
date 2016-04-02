import RPi.GPIO as GPIO

import time

from l293dne_motor import Motor

GPIO.setmode(GPIO.BOARD)

motor1 = Motor(38, 40)

while True:
    motor1.start_forward()
    time.sleep(0.7)
    motor1.stop()
    time.sleep(2)
    motor1.start_reverse()
    time.sleep(0.7)
    motor1.stop()
    time.sleep(2)
