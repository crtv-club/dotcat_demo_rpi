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

# Устанавливаем 40-й пин на вывод, на этот вывод подключена пищалка
GPIO.setup(40, GPIO.OUT)

# Устанавливаем 37-й пин на вход, сюда подключена кнопка
GPIO.setup(38, GPIO.IN)

# Бесконечный цикл
while True:

    # Пока кнопка нажата
    while GPIO.input(38):
        # Пищим: выводим попеременно 1-цу и ноль с высокой частотой (маленькой задержкой)

        # Выводим 1-цу на 40-й пин
        GPIO.output(40, GPIO.HIGH)

        # Ждем одну 561.6-ю секунды
        time.sleep(1 / 561.6)

        # Выводим ноль на 40-й пин
        GPIO.output(40, GPIO.LOW)

        # Ждем одну 561.6-ю секунды
        time.sleep(1 / 561.6)

# Убираем за собой: освобождаем пины
GPIO.cleanup()
