import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import requests
import serial

class EMLIFarmer(Node):
	def __init__(self):
		super().__init__('farmer_watcher_node')
		timer_period = 2 # seconds
		self.timer = self.create_timer(timer_period, self.timer_callback)
		self.esp_base_url = 'http://10.42.0.222/button/a/count'
		self.serial = serial.Serial('/dev/ttyACM0', 115200)

	def timer_callback(self):
		try:
			response = requests.get(self.esp_base_url)
			clicks = int(response.text)
			if clicks == 0:
				return

			self.pump_water()
			# log farmer watering
		except:
			print('Failed to get result')

	def pump_water(self):
		self.serial.write(b'p')
		self.serial.write(b'')

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
