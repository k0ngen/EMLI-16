import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from influxdb import InfluxDBClient
import requests

class EMLIPumpAlarm(Node):
	def __init__(self):
		super().__init__('emli_pump_water_alarm')
		self.subscription = self.create_subscription(
		String,
		'pump_water_alarm',
		self.listener_callback,
		10)
		self.subscription
		self.influx_client = InfluxDBClient(host='localhost', port=8086, database='plants')

	def listener_callback(self, msg):
		try:
			self.set_values(msg)
			self.save_value("pump_water_alarm", self.pump_water_alarm, self.timestamp)
		except:
			self.get_logger().info('Could not parse pump_water_alarm data')

	def set_values(self, msg):
		values = msg.data.split(",")
		self.pump_water_alarm = int(values[0])
		self.timestamp = int(values[1])

	def save_value(self, measurement, value, timestamp):
		data = [{"measurement": measurement,
			"fields": {"value": value},
			"time": timestamp}]
		self.influx_client.write_points(data)

def main(args=None):
	# initialize the node
	rclpy.init(args=args)
	# instantiate the subscriber class
	subscriber = EMLIPumpAlarm()
	# run the class
	rclpy.spin(subscriber)
	# destroy the class
	subscriber.destroy_node()
	rclpy.shutdown()

if __name__ == '__main__':
	main()
