import RPi.GPIO as GPIO


#sh_cp - сдвиг
#st_cp - синхро сигнал
#data_in - входные данные(1 или 0)
class ShiftRegistr(object):
    def __init__(self, data_in, sh_cp, st_cp):#обьявляем конструктор
        if type(data_in) != int or type(sh_cp) != int or type(st_cp):#проверка на правильность входных значений
            raise ValueError('Both arguments must be integers')

        self.data_in = data_in#инициализация переменной
        self.sh_cp = sh_cp#инициализация переменной
        self.st_cp = st_cp#инициализация переменной

        GPIO.setup(self.data_in, GPIO.OUT)#Установка пина подачи данных на выход
        GPIO.setup(self.sh_cp, GPIO.OUT)#Установка пина сдвига на выход
        GPIO.setup(self.st_cp, GPIO.OUT)#Установка пина синхросигнала на выход

    def __del__(self):#деструктор
        self.stop()#подаем на все пины нули
        GPIO.cleanup()#очищаем порты

    def stop(self):#Функция остановки
        GPIO.output(self.data_in, GPIO.LOW)#Устанавливаем пин в логический ноль
        GPIO.output(self.sh_cp, GPIO.LOW)#Устанавливаем пин в логический ноль
        GPIO.output(self.st_cp, GPIO.LOW)#Устанавливаем пин в логический ноль

    def clk_puls(self):#Делаем скачек импульса подавая сначала 0, потом 1, потом снова 0
        #для подачи сигнала что нам нужно сделать сдвиг
        GPIO.output(self.sh_cp, GPIO.LOW)#подаем на пин логичиеский 0
        GPIO.output(self.sh_cp, GPIO.HIGT)#подаем на пин логичискую 1
        GPIO.output(self.sh_cp, GPIO.LOW)#подаем на пин логичиеский 0

    def shift_reg(self, data):#Функция работы сдвига регистра
        for i in range(7):#Задаем диапазон от 0 до 7(по количеству выходов на нашем микроконтроллере, напомню, их 8)
            data_storage = -1# присваеваем -1, в случае ошибки записи в data_storage мы будем знать где ошибка
            if data & 0x80:#Проверяем контролирующий бит
                data_storage = 1#если он равен 1, записываем его в переменную и выходи из if-а
            else:#в противном случае переходим дальше, и присваеваем переменной data_torage ноль
                data_storage = 0
            data = data_storage << 1#Сдвигаем регистр на 1 влево и записываем в переменную, цикл начинаеться заново
            self.clk_puls()#даем импульс
        return data#возвращаем переменную

    def send_reg(self, data):#функция отправки данных на регистр
        GPIO.output(self.data_in, data)#отправляем данные
        self.synchr()#Передаем скачек сигналов, тем самым давая понять что мы все передали

    def synchr(self):#подаем сигнал синхроизациии(0 - 1 - 0)
        GPIO.output(self.st_cp, GPIO.LOW)#Подаем логический 0
        GPIO.output(self.st_cp, GPIO.HIGT)#Подаем логическую 1
        GPIO.output(self.st_cp, GPIO.LOW)#Подаем логический 0



