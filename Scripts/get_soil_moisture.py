import serial

connection = serial.Serial('/dev/ttyACM0', 115200)
values = connection.readline().decode().strip().split(",")
moisture = int(values[2])
print(moisture)
