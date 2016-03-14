#!/usr/bin/python

# Source: http://www.raspberrypi-spy.co.uk/2012/07/16x2-lcd-module-control-using-python/

# import
import RPi.GPIO as GPIO
import time

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

# Константы, определяют тип передаваемых данных в lcd_byte:
LCD_CHR = True   # LCD_CHR - передача символа
LCD_CMD = False  # LCD_CMD - передача команды

LCD_LINE_1 = 0x80  # Адрес оперативной памяти дисплея (!) для первой строки
LCD_LINE_2 = 0xC0  # Адрес оперативной памяти дисплея (!) для второй строки

# Временные константы
# Timing constants
E_PULSE = 0.0005  # Длина импульса (1-цы) на выводе LCD_E в lcd_toggle_enable
E_DELAY = 0.0005  # Задержка (????)


def main():
    """
    Основной блок программы
    Main program block
    :return: None
    """

    # Настраиваем порты:
    GPIO.setmode(GPIO.BOARD)      # Используем нумерацию GPIO.BOARD

    # Все порты к дисплею устанавливаем на вывод:
    GPIO.setup(LCD_E , GPIO.OUT)  # E
    GPIO.setup(LCD_RS, GPIO.OUT)  # RS
    GPIO.setup(LCD_D4, GPIO.OUT)  # DB4
    GPIO.setup(LCD_D5, GPIO.OUT)  # DB5
    GPIO.setup(LCD_D6, GPIO.OUT)  # DB6
    GPIO.setup(LCD_D7, GPIO.OUT)  # DB7

    # Инциализируем дисплей
    lcd_init()

    while True:
        # Выводим некоторый текст
        lcd_string("Rasbperry Pi", LCD_LINE_1)
        lcd_string("16x2 LCD Test", LCD_LINE_2)

        time.sleep(3)  # Задержка на 3 секунды

        # Send some text
        lcd_string("1234567890123456", LCD_LINE_1)
        lcd_string("abcdefghijklmnop", LCD_LINE_2)

        time.sleep(3)  # Задержка на 3 секунды

        # Выводим некоторый текст
        lcd_string("RaspberryPi-spy", LCD_LINE_1)
        lcd_string(".co.uk", LCD_LINE_2)

        time.sleep(3)

        # Выводим некоторый текст
        lcd_string("Follow me on", LCD_LINE_1)
        lcd_string("Twitter @RPiSpy", LCD_LINE_2)

        time.sleep(3)


def lcd_init():
    """
    Инициализируем дисплей
    :return: None
    """
    lcd_byte(0x33, LCD_CMD)  # 110011 Initialise
    lcd_byte(0x32, LCD_CMD)  # 110010 Initialise
    lcd_byte(0x06, LCD_CMD)  # 000110 Cursor move direction
    lcd_byte(0x0C, LCD_CMD)  # 001100 Display On,Cursor Off, Blink Off
    lcd_byte(0x28, LCD_CMD)  # 101000 Data length, number of lines, font size
    lcd_byte(0x01, LCD_CMD)  # 000001 Clear display
    time.sleep(E_DELAY)


def lcd_byte(bits, mode):
    """
    Отправляем байт данных на дисплей
    :param bits: сами данные, 8 бит информации
    :param mode: тип данных: True для чимволов и False для комманд
    :return: None
    """
    GPIO.output(LCD_RS, mode)  # Очищаем дисплей

    # Отправляем первые, верхние 4 бита данных
    # High bits

    # Устанавливаем выводы в ноль
    GPIO.output(LCD_D4, False)
    GPIO.output(LCD_D5, False)
    GPIO.output(LCD_D6, False)
    GPIO.output(LCD_D7, False)

    # Выводим единицы на выводы в соответствии с битами данных
    if bits & 0x10 == 0x10:        # Если четвертый бит - единица...
        GPIO.output(LCD_D4, True)  # высылаем 1-цу на порт D4.
    if bits & 0x20 == 0x20:        # Если третий бит - единица...
        GPIO.output(LCD_D5, True)  # высылаем 1-цу на порт D5.
    if bits & 0x40 == 0x40:        # Если второй бит - единица...
        GPIO.output(LCD_D6, True)  # высылаем 1-цу на порт D6.
    if bits & 0x80 == 0x80:        # Если первый бит - единица...
        GPIO.output(LCD_D7, True)  # высылаем 1-цу на порт D7.

    # Передергиваем вывод 'Enable'
    # Toggle 'Enable' pin
    lcd_toggle_enable()

    #############################################################################

    # Отправляем вторые, нижние 4 бита данных
    # Low bits

    # Устанавливаем выводы в ноль
    GPIO.output(LCD_D4, False)
    GPIO.output(LCD_D5, False)
    GPIO.output(LCD_D6, False)
    GPIO.output(LCD_D7, False)

    # Выводим единицы на выводы в соответствии с битами данных
    if bits & 0x01 == 0x01:        # Если восьмой бит - единица...
        GPIO.output(LCD_D4, True)  # высылаем 1-цу на порт D4.
    if bits & 0x02 == 0x02:        # Если седьмой бит - единица...
        GPIO.output(LCD_D5, True)  # высылаем 1-цу на порт D5.
    if bits & 0x04 == 0x04:        # Если шестой бит - единица...
        GPIO.output(LCD_D6, True)  # высылаем 1-цу на порт D6.
    if bits & 0x08 == 0x08:        # Если пятый бит - единица...
        GPIO.output(LCD_D7, True)  # высылаем 1-цу на порт D7.

    # Передергиваем вывод 'Enable'
    # Toggle 'Enable' pin
    lcd_toggle_enable()


def lcd_toggle_enable():
    """
    Передергивает пин 'Enable'
    :return: None
    """
    time.sleep(E_DELAY)

    GPIO.output(LCD_E, True)
    time.sleep(E_PULSE)

    GPIO.output(LCD_E, False)
    time.sleep(E_DELAY)


def lcd_string(message, line):
    """
    Отправляет строку на дисплей
    :param message: string, строка выводимого текста
    :param line: адрес памяти дисплея, куда произвести вывод;
                 у каждой строки дисплея - свой адрес памяти
    :return: None
    """
#напряжение между выводом потенцометра и общим выводом = 0.830 В
#сопротивление потенциометра 1й вывод = 8.280 кОм; 2й вывод = 1.67

    # Если строка длинее 16-ти символов (LCD_WIDTH)...
    message = message.ljust(LCD_WIDTH, " ")  # ...берем первые 16 символов и отбрасываем остальные

    # Высылаем команду: переключить вывод на строку line
    lcd_byte(line, LCD_CMD)

    # Высылаем строку текста, посимвольно:
    for i in range(LCD_WIDTH):

        # message[i] - берем i-й символ строки;
        # ord(message[i]) - берем код i-го символа в кодировке Unicode;
        # lcd_byte(...) - высылаем код символа на дисплей.
        lcd_byte(ord(message[i]), LCD_CHR)


if __name__ == '__main__':

    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        lcd_byte(0x01, LCD_CMD)
        lcd_string("Goodbye!", LCD_LINE_1)
        GPIO.cleanup()
