import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from influxdb import InfluxDBClient
import requests

class EMLISubscriber(Node):
	def __init__(self):
		super().__init__('emli_subscriber')
		self.subscription = self.create_subscription(
		String,
		'emli',
		self.listener_callback,
		10)
		self.esp_base_url = 'http://10.42.0.222/led'
		self.subscription # prevent unused variable warning
		self.influx_client = InfluxDBClient(host='localhost', port=8086, database='plants')

	def listener_callback(self, msg):
		self.set_values(msg)
		self.save_values()

		water_alarm = self.plant_water_alarm or not self.pump_water_alarm
		moisture_warning = self.moisture < 50
		no_alarms = not self.water_alarm and not self.moisture_warning

		self.toggle_green(no_alarms)
		self.toggle_yellow(moisture_warning)
		self.toggle_red(water_alarm)

		self.get_logger().info('I heard: "%s"' % values)

	def set_values(self, msg):
		values = msg.data.split(",")
		self.plant_water_alarm = int(values[0]) # 0 for no alarm
		self.pump_water_alarm = int(values[1]) # 1 for alarm
		self.moisture = int(values[2])
		self.light = int(values[3])
		
	def save_values(self, msg):
		timestamp = int(self.get_clock().now().nanoseconds / 1e9)
		self.save_value("plant_water_alarm", self.plant_water_alarm, timestamp)
		self.save_value("pump_water_alarm", self.pump_water_alarm, timestamp)
		self.save_value("moisture", self.moisture, timestamp)
		self.save_value("light", self.light, timestamp)

	def save_value(self, measurement, value, timestamp):
		data = [{"measurement": measurement,
			"fields": {measurement: value},
			"time": timestamp}]
		self.influx_client.write_points(data)

	def toggle_green(self, state):
		command = '/green/on' if state else '/green/off'
		requests.get(self.esp_base_url + command)

	def toggle_yellow(self, state):
		command = '/yellow/on' if state else '/yellow/off'
		requests.get(self.esp_base_url + command)

	def toggle_red(self, state):
		command = '/red/on' if state else '/red/off'
		requests.get(self.esp_base_url + command)

def main(args=None):
	# initialize the node
	rclpy.init(args=args)
	# instantiate the publisher class
	subscriber = EMLISubscriber()
	# run the class
	rclpy.spin(subscriber)
	# destroy the class
	subscriber.destroy_node()
	rclpy.shutdown()

if __name__ == '__main__':
	main()
