from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
	return LaunchDescription([
		Node(
			package='emli_package',
			executable='emli_sub_node',
			namespace='group1',
			name='emli_sub_node1'
		),
		Node(
			package='emli_package',
			executable='emli_farmer_node',
			namespace='group1',
			name='emli_farmer_node1'
		),
		Node(
			package='emli_package',
			executable='emli_light_node',
			namespace='group1',
			name='emli_light_node1'
		),
		Node(
			package='emli_package',
			executable='emli_moisture_node',
			namespace='group1',
			name='emli_moisture_node1'
		),
		Node(
			package='emli_package',
			executable='emli_water_alarm_node',
			namespace='group1',
			name='emli_water_alarm_node1'
		),
		Node(
			package='emli_package',
			executable='emli_pump_alarm_node',
			namespace='group1',
			name='emli_pump_alarm_node1'
		),
		Node(
			package='emli_package',
			executable='emli_pub_node',
			namespace='group1',
			name='emli_pub_node1'
		)
	])
