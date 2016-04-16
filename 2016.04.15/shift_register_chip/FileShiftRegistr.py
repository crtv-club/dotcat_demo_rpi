import RPi.GPIO as GPIO

# sh_cp - LATCH- сдвиг
# st_cp - CLK- синхро сигнал
# data_in - входные данные(1 или 0)
class ShiftRegister(object):
    def __init__(self, data_in, LATCH, CLK):  # обьявляем конструктор
        if type(data_in) != int or type(LATCH) != int or type(CLK) != int:  # проверка на правильность входных значений
            raise ValueError('Both arguments must be integers')

        self.data_in = data_in  # инициализация переменной
        self.LATCH = LATCH  # инициализация переменной
        self.CLK = CLK  # инициализация переменной

        GPIO.setup(self.data_in, GPIO.OUT)  # Установка пина подачи данных на выход
        GPIO.setup(self.LATCH, GPIO.OUT)  # Установка пина сдвига на выход
        GPIO.setup(self.CLK, GPIO.OUT)  # Установка пина синхросигнала на выход

    def __del__(self):  # деструктор
        self.stop()  # подаем на все пины нули
        GPIO.cleanup()  # очищаем порты

    def stop(self):  # Функция остановки
        GPIO.output(self.data_in, GPIO.LOW)  # Устанавливаем пин в логический ноль
        GPIO.output(self.LATCH, GPIO.LOW)  # Устанавливаем пин в логический ноль
        GPIO.output(self.CLK, GPIO.LOW)  # Устанавливаем пин в логический ноль
        return

    def clk_puls(self):  # Делаем скачек импульса подавая сначала 0, потом 1, потом снова 0
        # для подачи сигнала что нам нужно сделать сдвиг
        GPIO.output(self.CLK, GPIO.HIGH)  # подаем на пин логичискую 1
        GPIO.output(self.CLK, GPIO.LOW)  # подаем на пин логичиеский 0
        return

    def serLatch(self):
        GPIO.output(self.LATCH, GPIO.HIGH)
        # time.sleep(.01)
        GPIO.output(self.LATCH, GPIO.LOW)
        return

    def shift_reg(self, data):  # Функция работы сдвига регистра
        self.digital_write(GPIO.LOW)
        for i in range(0, 8):  # Задаем диапазон от 0 до 7(по количеству выходов на нашем микроконтроллере, напомню, их 8)
            temp = data & 0x80
            if temp & 0x80:  # Проверяем контролирующий бит
                GPIO.output(self.data_in, 1)  # если он равен 1, записываем его в переменную и выходи из if-а
            else:  # в противном случае переходим дальше, и присваеваем переменной data_torage ноль
                GPIO.output(self.data_in, 0)
            self.clk_puls()
            data = data << 1  # Сдвигаем регистр на 1 влево и записываем в переменную, цикл начинаеться заново
        self.serLatch()
        return

    def convBinary(self, value):
        binaryValue = '0b'
        for x in range(0, 8):
            temp = value & 0x80
            if temp == 0x80:
                binaryValue = binaryValue + '1'
            else:
                binaryValue = binaryValue + '0'
            value = value << 1
        return binaryValue
