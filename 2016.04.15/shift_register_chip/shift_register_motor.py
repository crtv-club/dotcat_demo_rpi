import RPi.GPIO as GPIO
from FileShiftRegistr import ShiftRegistr

# устанавливаем пины
data_in = 3  # пин для входных данных
st_cp = 5  # пин для синхросигнала
sh_cp = 7  # пин для сдвига

Data = 0b10011100 #
# которое будем менять для работы определенных моторов/диодов
GPIO.setmode(GPIO.BOARD)  # устанавливаем режим пинов

RegistrForDiods = ShiftRegistr(data_in, sh_cp, st_cp)

while True:
 temp = RegistrForDiods.converBinary(Data)
 RegistrForDiods.shift_reg(temp)
