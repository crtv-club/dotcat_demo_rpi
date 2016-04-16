import RPi.GPIO as GPIO
from shift_reg_lib import ShiftRegister
from time import sleep

# устанавливаем пины
si = 37    # пин для входных данных
rck = 33   # пин для сдвига регистров хранения
sck = 35   # пин для синхросигнала и сдвига
sclr = 40  # пин для очистки

Data = 0b01010101
# которое будем менять для работы определенных моторов/диодов
GPIO.setmode(GPIO.BOARD)  # устанавливаем режим пинов

diode_reg = ShiftRegister(si, sck, rck, sclr)

while True:
    diode_reg.write_data(Data)
    sleep(1)
    diode_reg.write_data(~ Data)
    sleep(1)
