import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import requests

class EMLISubscriber(Node):
	def __init__(self):
		super().__init__('emli_subscriber')
		self.subscription = self.create_subscription(
		String,
		'emli',
		self.listener_callback,
		10)
		self.light_publisher = self.create_publisher(String, 'light', 10)
		self.moisture_publisher = self.create_publisher(String, 'moisture', 10)
		self.plant_water_alarm_publisher = self.create_publisher(String, 'plant_water_alarm', 10)
		self.pump_water_alarm_publisher = self.create_publisher(String, 'pump_water_alarm', 10)
		self.esp_base_url = 'http://10.42.0.222/led'
		self.subscription # prevent unused variable warning

	def listener_callback(self, msg):
		try:
			self.set_values(msg)
			self.publish_values()

			water_alarm = self.plant_water_alarm or not self.pump_water_alarm
			moisture_warning = self.moisture < 50
			no_alarms = not water_alarm and not moisture_warning

			self.toggle_green(no_alarms)
			self.toggle_yellow(moisture_warning)
			self.toggle_red(water_alarm)
		except Exception as e:
			self.get_logger().info('Could not parse data %s' % str(e))

	def set_values(self, msg):
		values = msg.data.split(",")
		self.plant_water_alarm = int(values[0]) # 0 for no alarm
		self.pump_water_alarm = int(values[1]) # 1 for alarm
		self.moisture = int(values[2])
		self.light = int(values[3])

	def publish_values(self):
		timestamp = self.get_clock().now().nanoseconds

		plant_water_alarm_msg = String()
		plant_water_alarm_msg.data = str("{},{}".format(self.plant_water_alarm, timestamp))
		self.plant_water_alarm_publisher.publish(plant_water_alarm_msg)

		pump_water_alarm_msg = String()
		pump_water_alarm_msg.data = str("{},{}".format(self.pump_water_alarm, timestamp))
		self.pump_water_alarm_publisher.publish(pump_water_alarm_msg)

		moisture_msg = String()
		moisture_msg.data = str("{},{}".format(self.moisture, timestamp))
		self.moisture_publisher.publish(moisture_msg)

		light_msg = String()
		light_msg.data = str("{},{}".format(self.light, timestamp))
		self.light_publisher.publish(light_msg)

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
