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
		self.esp_url = 'http://10.42.0.222'
		self.subscription # prevent unused variable warning
		self.influx_client = InfluxDBClient(host='localhost', port=8086, database='plants')
	def listener_callback(self, msg):
		values = msg.data.split(",")
		plant_water_alarm = int(values[0]) # 0 for no alarm
		pump_water_alarm = int(values[1]) # 1 for alarm
		moisture = int(values[2])
		light = int(values[3])

		timestamp = int(self.get_clock().now().nanoseconds / 1e9)

		self.save_value("plant_water_alarm", plant_water_alarm, timestamp)
		self.save_value("pump_water_alarm", pump_water_alarm, timestamp)
		self.save_value("moisture", moisture, timestamp)
		self.save_value("light", light, timestamp)

		water_alarm = plant_water_alarm or not pump_water_alarm
		moisture_warning = moisture < 50
		no_alarms = not water_alarm and not moisture_warning

		if no_alarms:
			self.toggle_green(True)
			return

		if moisture_warning:
			self.toggle_yellow(True)
		else:
			self.toggle_yellow(False)

		if water_alarm:
			self.toggle_red(True)
		else:
			self.toggle_red(False)

		self.get_logger().info('I heard: "%s"' % values)

	def save_value(self, measurement, value, timestamp):
		data = [{"measurement": measurement,
			"fields": {measurement: value},
			"time": timestamp}]
		self.influx_client.write_points(data)

	def toggle_red(self, state):
		if state:
			self.toggle_green(False)

		base = '/led/red/'
		base += 'on' if state else 'off'
		requests.get(self.esp_url + base)

	def toggle_yellow(self, state):
		if state:
			self.toggle_green(False)

		base = '/led/yellow/'
		base += 'on' if state else 'off'
		requests.get(self.esp_url + base)

	def toggle_green(self, state):
		if state:
			self.toggle_red(False)
			self.toggle_yellow(False)

		base = '/led/green/'
		base += 'on' if state else 'off'
		requests.get(self.esp_url + base)

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
