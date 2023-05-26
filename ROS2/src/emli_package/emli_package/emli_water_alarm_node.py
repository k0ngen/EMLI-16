import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from influxdb import InfluxDBClient
import requests

class EMLIWaterAlarm(Node):
	def __init__(self):
		super().__init__('emli_plant_water_alarm')
		self.subscription = self.create_subscription(
		String,
		'plant_water_alarm',
		self.listener_callback,
		10)
		self.subscription # prevent unused variable warning
		self.influx_client = InfluxDBClient(host='localhost', port=8086, database='plants')

	def listener_callback(self, msg):
		try:
			self.set_values(msg)
			self.save_value("plant_water_alarm", self.plant_water_alarm, self.timestamp)
		except:
			self.get_logger().info('Could not parse plant_water_alarm data')

	def set_values(self, msg):
		values = msg.data.split(",")
		self.plant_water_alarm = int(values[0])
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
	subscriber = EMLIWaterAlarm()
	# run the class
	rclpy.spin(subscriber)
	# destroy the class
	subscriber.destroy_node()
	rclpy.shutdown()

if __name__ == '__main__':
	main()
