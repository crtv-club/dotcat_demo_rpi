def OpenAndReadFile( _file ):
    TempOpenFile = open( _file )
    tempText = TempOpenFile.read()
    TempOpenFile.close()
    return tempText

def SplitDataForTemperatureSensor( _file ):
    TempData = OpenAndReadFile( _file )
    SplitData = TempData.split("\n")[1].split(" ")[9]
    temperature = float(SplitData[2:])/1000
    return temperature