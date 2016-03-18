# Мигаем светодиодом

# Библиотека для работы с портами ввода-вывода
# (одна из них). Источник: https://pypi.python.org/pypi/RPi.GPIO
import RPi.GPIO as GPIO  # Выполняем импорт под именем GPIO

# Функция sleep содержится в библиотеке time,
# подгружаем всю библиотеку
import time

# Устанавливаем метод нумерования портов: BCM или BOARD
# Подробнее: http://makezine.com/projects/tutorial-raspberry-pi-gpio-pins-and-python/
GPIO.setmode(GPIO.BOARD)

# Устанавливаем 40-й пин на вывод
GPIO.setup(40, GPIO.OUT)

# Устанавливаем высокий уровень сигнала (1-цу) на 40-й пин
GPIO.output(40, GPIO.HIGH)  # Светодиод загорается

# Ждем 5 секунд
time.sleep(5)

# Устанавливаем низкий уровень сигнала (ноль) на 40-й пин
GPIO.output(40, GPIO.LOW)  # Светодиод выключается

# Убираем за собой: освобождаем пины
GPIO.cleanup()
