import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import serial

class EMLIPublisher(Node):
	def __init__(self):
		super().__init__('emli_publisher')
		self.publisher_ = self.create_publisher(String, 'emli', 10)
		timer_period = 1 # seconds
		self.timer = self.create_timer(timer_period, self.timer_callback)
		self.serial = serial.Serial('/dev/ttyACM0', 115200)

	def timer_callback(self):
		try:
			msg = String()
			msg.data = self.serial.readline().decode().strip()
			self.publisher_.publish(msg)
			self.get_logger().info('Publishing: "%s"' % msg.data)
		except:
			self.get_logger().info('Could not read data')

def main(args=None):
	# initialize the node
	rclpy.init(args=args)
	# instantiate the publisher class
	publisher = EMLIPublisher()
	# run the class
	rclpy.spin(publisher)
	# destroy the class
	publisher.destroy_node()
	rclpy.shutdown()

if __name__ == '__main__':
	main()
