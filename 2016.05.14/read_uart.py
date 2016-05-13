import serial

ser = serial.Serial("/dev/ttyACM0")  # Open named port
ser.baudrate = 9600  # Set baud rate to 9600
while 1:
    data = ser.readline()  # Read line from serial port to data
    print(data)  # Print the received data

ser.close()
