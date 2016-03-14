import RPi.GPIO as GPIO
import time

def set_constants(
        rs, e, d4, d5, d6, d7,
        width, chr, cmd, line_1, line_2,
        e_pulse, e_delay
):
    global LCD_RS, LCD_E, LCD_D4, LCD_D5, LCD_D6, LCD_D7, LCD_WIDTH, LCD_CHR, LCD_CMD, LCD_LINE_1, LCD_LINE_2, E_PULSE, E_DELAY

    # Определяем номера портов, на которые подключен дисплей
    # Define GPIO to LCD mapping
    LCD_RS = rs
    LCD_E  = e
    LCD_D4 = d4
    LCD_D5 = d5
    LCD_D6 = d6
    LCD_D7 = d7

    # Define some device constants
    LCD_WIDTH = width  # Максимальное количество символов в строке

    # Константы, определяют тип передаваемых данных в byte:
    LCD_CHR = chr   # LCD_CHR - передача символа
    LCD_CMD = cmd  # LCD_CMD - передача команды

    LCD_LINE_1 = line_1  # Адрес оперативной памяти дисплея (!) для первой строки
    LCD_LINE_2 = line_2  # Адрес оперативной памяти дисплея (!) для второй строки

    # Временные константы
    # Timing constants
    E_PULSE = e_pulse  # Длина импульса (1-цы) на выводе LCD_E в toggle_enable
    E_DELAY = e_delay  # Задержка (????)


def init():
    # Initialise display
    byte(0x33, LCD_CMD)  # 110011 Initialise
    byte(0x32, LCD_CMD)  # 110010 Initialise
    byte(0x06, LCD_CMD)  # 000110 Cursor move direction
    byte(0x0C, LCD_CMD)  # 001100 Display On,Cursor Off, Blink Off
    byte(0x28, LCD_CMD)  # 101000 Data length, number of lines, font size
    byte(0x01, LCD_CMD)  # 000001 Clear display
    time.sleep(E_DELAY)


def byte(bits, mode):
    # Send byte to data pins
    # bits = data
    # mode = True  for character
    #        False for command

    GPIO.output(LCD_RS, mode)  # RS

    # High bits
    GPIO.output(LCD_D4, False)
    GPIO.output(LCD_D5, False)
    GPIO.output(LCD_D6, False)
    GPIO.output(LCD_D7, False)
    if bits & 0x10 == 0x10:
        GPIO.output(LCD_D4, True)
    if bits & 0x20 == 0x20:
        GPIO.output(LCD_D5, True)
    if bits & 0x40 == 0x40:
        GPIO.output(LCD_D6, True)
    if bits & 0x80 == 0x80:
        GPIO.output(LCD_D7, True)

    # Toggle 'Enable' pin
    toggle_enable()

    # Low bits
    GPIO.output(LCD_D4, False)
    GPIO.output(LCD_D5, False)
    GPIO.output(LCD_D6, False)
    GPIO.output(LCD_D7, False)
    if bits & 0x01 == 0x01:
        GPIO.output(LCD_D4, True)
    if bits & 0x02 == 0x02:
        GPIO.output(LCD_D5, True)
    if bits & 0x04 == 0x04:
        GPIO.output(LCD_D6, True)
    if bits & 0x08 == 0x08:
        GPIO.output(LCD_D7, True)

    # Toggle 'Enable' pin
    toggle_enable()


def toggle_enable():
    # Toggle enable
    time.sleep(E_DELAY)
    GPIO.output(LCD_E, True)
    time.sleep(E_PULSE)
    GPIO.output(LCD_E, False)
    time.sleep(E_DELAY)


def string(message, line):
    # Send string to display

    message = message.ljust(LCD_WIDTH, " ")

    byte(line, LCD_CMD)

    for i in range(LCD_WIDTH):
        byte(ord(message[i]), LCD_CHR)
