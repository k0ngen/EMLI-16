import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import requests
import serial
from influxdb import InfluxDBClient

class EMLIFarmer(Node):
	def __init__(self):
		super().__init__('farmer_watcher_node')
		timer_period = 2 # seconds
		self.timer = self.create_timer(timer_period, self.timer_callback)
		self.esp_base_url = 'http://10.42.0.222/button/a/count'
		self.serial = serial.Serial('/dev/ttyACM0', 115200)
		self.influx_client = InfluxDBClient(host='localhost', port=8086, database='plants')

	def timer_callback(self):
		try:
			response = requests.get(self.esp_base_url)
			clicks = int(response.text)
			if clicks == 0:
				return

			try:
				self.pump_water()
			except:
				self.pump_water()

			self.log_watering()
		except:
			print('Failed to get result')

	def pump_water(self):
		self.serial.write(b'p')
		self.serial.write(b'')

	def log_watering(self):
		data = [{"measurement": "watering",
                	"fields": {"value": "farmer"},
                	"time": self.get_clock().now().nanoseconds}]
		self.influx_client.write_points(data)


def main(args=None):
	# initialize the node
	rclpy.init(args=args)
	# instantiate the publisher class
	publisher = EMLIFarmer()
	# run the class
	rclpy.spin(publisher)
	# destroy the class
	publisher.destroy_node()
	rclpy.shutdown()

if __name__ == '__main__':
	main()
