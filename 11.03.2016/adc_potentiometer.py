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

# Пин, на который подключена пищалка
BUZZER_PIN = 40

# Устанавливаем пин пищалки на вывод
GPIO.setup(BUZZER_PIN, GPIO.OUT)

# Максимальная частота в герцах.
# Именно на этой частоте будет звучать пищалка, когда мы потенциометр выкрутим на максимум
MAX_FREQ = 400  # Hz

# Про ШИМ в RPi.GPIO: https://sourceforge.net/p/raspberry-gpio-python/wiki/PWM/

# Создаем экземпляр класса ШИМ.
# Через этот объект мы будем выводить сигнал на пин BUZZER_PIN с некоторой частотой
buzzer_pwm = GPIO.PWM(BUZZER_PIN, MAX_FREQ)

# Устанавливаем режимы пинов интерфейса SPI
# set up the SPI interface pins
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)

# 10k trim pot connected to adc #0
# Потенциометр подключен на нулевой вход АЦП
potentiometer_adc = 0

last_read = 0       # Переменная отслеживает последнее считанное с потенциометра значение
tolerance = 7       # Минимальное изменение значения. Новое значение с потенциометра будем
                    # считывать только тогда, когда разница между текущим и предудущим значением
                    # будет больше tolerance. Необходимо для устранения дребезжания

# Начинаем пищать. 50.0 - процент времени, на протяжении которого будем держать на пине 1-цу
buzzer_pwm.start(50.0)

# Основной бесконечный цикл
while True:
        # Будем считать, что потенциометр не изменил положение
        # we'll assume that the pot didn't move
        trim_pot_changed = False

        # Считываем очередное значение с АЦП
        # read the analog pin
        trim_pot = adc.readadc(potentiometer_adc, SPICLK, SPIMOSI, SPIMISO, SPICS)

        # Вычисляем разницу между текущим и прошлым значением
        # how much has it changed since the last read?
        pot_adjust = abs(trim_pot - last_read)

        # Если изменение больше tolerance
        if pot_adjust > tolerance:
               # Считаем, что потенциометр изменил положение
               trim_pot_changed = True

        # Если потенциометр повернулся...
        if ( trim_pot_changed ):
                set_frequency = trim_pot / 10.24           # преобразовываем 10-битное значение adc0 (0-1024) в значение
                                                           # процента частоты (от 0 до 100)
                set_frequency = round(set_frequency, 2)    # Округляем полученное значение до сотых
                #set_frequency = int(set_frequency)        # cast volume as integer

                print('Frequency = {freq}%' .format(freq = set_frequency))  # выводим новое значение частоты на экран

                buzzer_pwm.ChangeFrequency(  # Изменяем частоту пищания на...
                        max(
                            MAX_FREQ * set_frequency / 100.0,  # ...произведение максимальной частоты на процент
                            1  # ...либо на 1Гц, если потенциометр будет установлен в ноль
                        )
                )

                # Сохраняем последнее считанное значение до следующей итерации
                # save the potentiometer reading for the next loop
                last_read = trim_pot

        # Ничего не делаем 1/10-ю секунды
        # hang out and do nothing for a 1/10th of second
        time.sleep(0.1)
