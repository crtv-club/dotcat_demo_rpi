#!/usr/bin/python

# Source: http://www.raspberrypi-spy.co.uk/2012/07/16x2-lcd-module-control-using-python/

# import
import RPi.GPIO as GPIO
import time

import lcd
import adc

# Настраиваем порты:
GPIO.setmode(GPIO.BOARD)      # Используем нумерацию GPIO.BOARD

# Определяем номера портов, на которые подключен дисплей
# Define GPIO to LCD mapping
LCD_RS = 13
LCD_E  = 15
LCD_D4 = 37
LCD_D5 = 33
LCD_D6 = 36
LCD_D7 = 32

# Define some device constants
LCD_WIDTH = 16  # Максимальное количество символов в строке

# Константы, определяют тип передаваемых данных в display.lcd.byte:
LCD_CHR = True   # LCD_CHR - передача символа
LCD_CMD = False  # LCD_CMD - передача команды

LCD_LINE_1 = 0x80  # Адрес оперативной памяти дисплея (!) для первой строки
LCD_LINE_2 = 0xC0  # Адрес оперативной памяти дисплея (!) для второй строки

# Временные константы
# Timing constants
E_PULSE = 0.0005  # Длина импульса (1-цы) на выводе LCD_E в display.lcd.toggle_enable
E_DELAY = 0.0005  # Задержка (????)

lcd.set_constants(
        LCD_RS, LCD_E, LCD_D4, LCD_D5, LCD_D6, LCD_D7,
        LCD_WIDTH, LCD_CHR, LCD_CMD, LCD_LINE_1, LCD_LINE_2,
        E_PULSE, E_DELAY
)

# Номера портов, которые будут использованый для SPI. Сюда будет подключен АЦП
# SPI port on the ADC to the Cobbler
SPICLK = 12
SPIMISO = 16
SPIMOSI = 18
SPICS = 22

def main():
    """
    Основной блок программы
    Main program block
    :return: None
    """

    # 10k trim pot connected to adc #1
    # Потенциометр подключен на первый вход АЦП
    potentiometer_adc = 7

    last_read = 0       # Переменная отслеживает последнее считанное с потенциометра значение
    tolerance = 7       # Минимальное изменение значения. Новое значение с потенциометра будем
                        # считывать только тогда, когда разница между текущим и предудущим значением
                        # будет больше tolerance. Необходимо для устранения дребезжания

    MAX_VALUE = 1023

    #####################################################################

    # Все порты к дисплею устанавливаем на вывод:
    GPIO.setup(LCD_E , GPIO.OUT)  # E
    GPIO.setup(LCD_RS, GPIO.OUT)  # RS
    GPIO.setup(LCD_D4, GPIO.OUT)  # DB4
    GPIO.setup(LCD_D5, GPIO.OUT)  # DB5
    GPIO.setup(LCD_D6, GPIO.OUT)  # DB6
    GPIO.setup(LCD_D7, GPIO.OUT)  # DB7

    # Инциализируем дисплей
    lcd.init()

    # Устанавливаем режимы пинов интерфейса SPI
    # set up the SPI interface pins
    GPIO.setup(SPIMOSI, GPIO.OUT)
    GPIO.setup(SPIMISO, GPIO.IN)
    GPIO.setup(SPICLK, GPIO.OUT)
    GPIO.setup(SPICS, GPIO.OUT)

    potentiometer_adc = 7

    last_read = 0       # Переменная отслеживает последнее считанное с потенциометра значение
    tolerance = 7       # Минимальное изменение значения. Новое значение с потенциометра будем
                        # считывать только тогда, когда разница между текущим и предудущим значением
                        # будет больше tolerance. Необходимо для устранения дребезжания


    while True:
        user_input = input()

        if user_input == 'e':
            break

        # Считываем очередное значение с АЦП
        hum_raw_value = adc.readadc(potentiometer_adc, SPICLK, SPIMOSI, SPIMISO, SPICS)

        hum_value = abs(hum_raw_value - 1023)

        percent = round(hum_value * 100.0 / MAX_VALUE)

        lcd.string(' Humidity = {hum}%' .format(hum = percent), LCD_LINE_1)


if __name__ == '__main__':

    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        lcd.byte(0x01, LCD_CMD)
        lcd.string("Goodbye!", LCD_LINE_1)
        GPIO.cleanup()
