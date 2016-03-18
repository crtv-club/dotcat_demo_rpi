#!/usr/bin/python

# Source: http://www.raspberrypi-spy.co.uk/2012/07/16x2-lcd-module-control-using-python/

# import
import RPi.GPIO as GPIO
import time

import lcd

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

# Константы, определяют тип передаваемых данных в lcd.byte:
LCD_CHR = True   # LCD_CHR - передача символа
LCD_CMD = False  # LCD_CMD - передача команды

LCD_LINE_1 = 0x80  # Адрес оперативной памяти дисплея (!) для первой строки
LCD_LINE_2 = 0xC0  # Адрес оперативной памяти дисплея (!) для второй строки

# Временные константы
# Timing constants
E_PULSE = 0.0005  # Длина импульса (1-цы) на выводе LCD_E в lcd.toggle_enable
E_DELAY = 0.0005  # Задержка (????)

lcd.set_constants(
        LCD_RS, LCD_E, LCD_D4, LCD_D5, LCD_D6, LCD_D7,
        LCD_WIDTH, LCD_CHR, LCD_CMD, LCD_LINE_1, LCD_LINE_2,
        E_PULSE, E_DELAY
)

def main():
    """
    Основной блок программы
    Main program block
    :return: None
    """

    # Все порты к дисплею устанавливаем на вывод:
    GPIO.setup(LCD_E , GPIO.OUT)  # E
    GPIO.setup(LCD_RS, GPIO.OUT)  # RS
    GPIO.setup(LCD_D4, GPIO.OUT)  # DB4
    GPIO.setup(LCD_D5, GPIO.OUT)  # DB5
    GPIO.setup(LCD_D6, GPIO.OUT)  # DB6
    GPIO.setup(LCD_D7, GPIO.OUT)  # DB7

    # Инциализируем дисплей
    lcd.init()

    while True:
        # Выводим некоторый текст
        lcd.string("Rasbperry Pi", LCD_LINE_1)
        lcd.string("16x2 LCD Test", LCD_LINE_2)

        time.sleep(3)  # Задержка на 3 секунды

        # Send some text
        lcd.string("1234567890123456", LCD_LINE_1)
        lcd.string("abcdefghijklmnop", LCD_LINE_2)

        time.sleep(3)  # Задержка на 3 секунды

        # Выводим некоторый текст
        lcd.string("RaspberryPi-spy", LCD_LINE_1)
        lcd.string(".co.uk", LCD_LINE_2)

        time.sleep(3)

        # Выводим некоторый текст
        lcd.string("Follow me on", LCD_LINE_1)
        lcd.string("Twitter @RPiSpy", LCD_LINE_2)

        time.sleep(3)

if __name__ == '__main__':

    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        lcd.byte(0x01, LCD_CMD)
        lcd.string("Goodbye!", LCD_LINE_1)
        GPIO.cleanup()