import RPi.GPIO as GPIO
from shift_reg_lib import ShiftRegister
from time import sleep

# устанавливаем пины
si = 37    # пин для входных данных
rck = 33   # пин для сдвига регистров хранения
sck = 35   # пин для синхросигнала и сдвига
sclr = 40  # пин для очистки

Data = 0b10101010
off = 0b00000000
on = 0b11111111
# которое будем менять для работы определенных моторов/диодов
GPIO.setmode(GPIO.BOARD)  # устанавливаем режим пинов

diode_reg = ShiftRegister(si, sck, rck, sclr)
#while True:
#diode_reg.clear()
diode_reg.write_data(off)
sleep(10)
#
 #   diode_reg.write_data(off)
  #  sleep(20)
