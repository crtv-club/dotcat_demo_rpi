# Подобие PWM: плавно изменяем "яркость" светодиода

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

# Устанавливаем максимальный делитель для времени свечения диода
maxdivider = 500

# Устанавливаем шаг изменения делителя
step = maxdivider * 0.001

# Начальное значения делителя равно шагу
i = step

# Пока делитель не достигнет максимума
while i < maxdivider:
    # Выводим попеременно 1-цу и ноль

    # Выводим 1-цу на 40-й пин (включаем диод)
    GPIO.output(40, GPIO.HIGH)

    # Ждем одну (maxdivider - i)-ю секунд
    time.sleep(1 / (maxdivider - i))

    # Выводим ноль на 40-й пин
    GPIO.output(40, GPIO.LOW)

    # Ждем i-ю секунд
    time.sleep(1 / i)

    # Увеличиваем значение делителя
    i += step


# Убираем за собой: освобождаем пины
GPIO.cleanup()
