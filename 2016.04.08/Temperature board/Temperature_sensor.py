import time

def OpenAndReadFile( _file ):
    TempOpenFile = open( _file )
    file = TempOpenFile.read()
    TempOpenFile.close()
    return file


def SplitDataForTemperatureSensor( _file ):
    TempData = OpenAndReadFile( _file )
    SplitData = TempData.split("\n")[1].split(" ")[9]
    temperature = float(SplitData[2:])/1000
    return temperature

while(True):
    print(SplitDataForTemperatureSensor('/sys/bus/w1/devices/28-000003d38d8c/w1_slave'))
    time.sleep(1)

