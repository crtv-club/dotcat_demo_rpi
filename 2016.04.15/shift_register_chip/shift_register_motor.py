from FileShiftRegistr import ShiftRegistr
import RPi.GPIO as GPIO
#устанавливаем пины
data_in = 3# пин для входных данных
st_cp = 5#пин для синхросигнала
sh_cp = 7#пин для сдвига

Data = 0x80# восьмибитное значения
#которое будем менять для работы определенных моторов/диодов
GPIO.setmode(GPIO.BOARD) #устанавливаем режим пинов


RegistrForMotor = ShiftRegistr(data_in, sh_cp, st_cp)#конструируем объект регистра RegistrForMotor

while True:
    DataForSendToController = RegistrForMotor.shift_reg(Data)#записываем значения
    #которое должны подать в DataForSendToController
    RegistrForMotor.send_reg(DataForSendToController)#отправляем значения на контроллер


