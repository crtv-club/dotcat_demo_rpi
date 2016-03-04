# Библиотека для работы с портами ввода-вывода
# (одна из них). Источник: https://pypi.python.org/pypi/RPi.GPIO
import RPi.GPIO as GPIO  # Выполняем импорт под именем GPIO

# Функция sleep содержится в библиотеке time,
# подгружаем одну функцию sleep из библиотеки
from time import sleep

# Устанавливаем метод нумерования портов: BCM или BOARD
# Подробнее: http://makezine.com/projects/tutorial-raspberry-pi-gpio-pins-and-python/
GPIO.setmode(GPIO.BOARD)

# Настраиваем 37-й вывод на вход
GPIO.setup(37, GPIO.IN)

# Обычный бесконечный цикл
while True:
    # Считываем значение с 37-го вывода
    if GPIO.input(37):
        # Если функция вернула HIGH (оно же 1, оно же True)...
        print("Movement detected")
    else:
        # ...иначе...
        print("No movement")

    # Ждем пол-секунды перед началом новой итерации
    sleep(0.5)

# Освобождаем пины
GPIO.cleanup()
