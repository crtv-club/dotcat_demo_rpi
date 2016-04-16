import RPi.GPIO as GPIO
from FileShiftRegistr import ShiftRegister
import time
# устанавливаем пины
data_in = 37  # пин для входных данных
st_cp = 33  # пин для синхросигнала
sh_cp = 35  # пин для сдвига

Data = 0b01010101
# которое будем менять для работы определенных моторов/диодов
GPIO.setmode(GPIO.BOARD)  # устанавливаем режим пинов

RegistrForDiods = ShiftRegister(data_in, sh_cp, st_cp)


while 1:
    temp = 0b0111
    RegistrForDiods.shift_reg(temp)

    #for i in range(0, 8):
    #    RegistrForDiods.shift_reg(temp)
    #    temp = temp << 1
    #    time.sleep(0.5)

