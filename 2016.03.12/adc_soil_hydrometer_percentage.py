# Based on: http://bit.ly/226GBjt (Limor "Ladyada" Fried for Adafruit Industries, (c) 2015)


import RPi.GPIO as GPIO
import time

import adc

# Используем нумерацию выводов по типу GPIO.BOARD,
# подробнее: http://bit.ly/1pC3VEs
GPIO.setmode(GPIO.BOARD)

# Номера портов, которые будут использованы для SPI. Сюда будет подключен АЦП
# SPI port on the ADC to the Cobbler
SPICLK = 12
SPIMISO = 16
SPIMOSI = 18
SPICS = 22

# Устанавливаем режимы пинов интерфейса SPI
# set up the SPI interface pins
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)

# 10k trim pot connected to adc #7
# Сенсор подключен на седьмой вход АЦП
hydr_adc = 7

last_read = 0       # Переменная отслеживает последнее считанное с потенциометра значение
tolerance = 7       # Минимальное изменение значения. Новое значение с потенциометра будем
                    # считывать только тогда, когда разница между текущим и предудущим значением
                    # будет больше tolerance. Необходимо для устранения дребезжания

MAX_VALUE = 1023

# Основной бесконечный цикл
while True:
        user_input = input()

        if user_input == 'e':
            break

        # Считываем очередное значение с АЦП
        # read the analog pin
        hum_raw_value = adc.readadc(hydr_adc, SPICLK, SPIMOSI, SPIMISO, SPICS)

        hum_value = abs(hum_raw_value - 1023)

        percent = round(hum_value * 100.0 / MAX_VALUE)

        print(hydr_adc, ' Humidity = {hum}%' .format(hum = percent))  # выводим новое значение частоты на экран

        # Ничего не делаем 1/10-ю секунды
        # hang out and do nothing for a 1/10th of second
        time.sleep(0.1)

GPIO.cleanup()
