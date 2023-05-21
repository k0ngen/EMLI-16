import serial
import time
from influxdb import InfluxDBClient

def can_water():
	values = connection.readline().decode().strip().split(",")
	plant_water_alarm = int(values[0])
	pump_water_alarm = int(values[1])
	water_alarm = plant_water_alarm or not pump_water_alarm
	return not water_alarm

def water():
	connection.write(b'p')
	connection.write(b'')

def log_watering():
	data = [{"measurement": "watering",
                "fields": {"value": "rpi"},
                "time": time.time_ns()}]
	influx_client.write_points(data)

connection = serial.Serial('/dev/ttyACM0', 115200)
influx_client = InfluxDBClient(host='localhost', port=8086, database='plants')
if can_water():
	water()
	log_watering()
