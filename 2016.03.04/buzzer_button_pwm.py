# Пищим по нажатию на кнопку

# Библиотека для работы с портами ввода-вывода
# (одна из них). Источник: https://pypi.python.org/pypi/RPi.GPIO
import RPi.GPIO as GPIO

# Функция sleep содержится в библиотеке time,
# подгружаем всю библиотеку
import time

# Устанавливаем метод нумерования портов: BCM или BOARD
# Подробнее: http://makezine.com/projects/tutorial-raspberry-pi-gpio-pins-and-python/
GPIO.setmode(GPIO.BOARD)

# Задаем константу: номер пина, на которую подключена пищалка (для удобства)
buzzer_pin = 40

# Задаем константу: номер пина, на которую подключена кнопка (для удобства)
button_pin = 38

# Устанавливаем пин с пищалкой на вывод
GPIO.setup(buzzer_pin, GPIO.OUT)

# Устанавливаем 38-й пин на вход, сюда подключена кнопка
GPIO.setup(button_pin, GPIO.IN)

# Создаем объект класса PWM
buzzer_pwm = GPIO.PWM(    # В конструктор передаем:
    buzzer_pin,  # номер пина, который мы будем использовать для PWM
    261.626      # частота в герцах
)

# Бесконечный цикл
while True:
    # Ждем, пока кто-то нажмет на кнопку (передний фронт)
    GPIO.wait_for_edge(button_pin, GPIO.RISING, timeout=5000)

    # Начинаем пищать
    buzzer_pwm.start(50.0)  # аргумент - сколько времени держать 1-цу на выходе (в процентах)

    # Ждем, пока кто-то отпустит кнопку (задний фронт)
    GPIO.wait_for_edge(button_pin, GPIO.FALLING, timeout=5000)

    # Перестаем пищать
    buzzer_pwm.stop()


# Убираем за собой: освобождаем пины
GPIO.cleanup()
