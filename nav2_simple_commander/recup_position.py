from rclpy.node import Node
from sensor_msgs.msg import LaserScan
import nav2_simple_commander.constants as c
import math
import time
import geometry_msgs.msg
from rclpy.qos import qos_profile_sensor_data
import nav2_simple_commander.navigation_goal as ng

class Initial_position(Node):
    def __init__(self):
        super().__init__("Récup position")
        print("On cherche à récupérer la position initiale")
        self.subscription = self.create_subscription(
            LaserScan,
            '/scan',
            self.listener_callback,
            qos_profile_sensor_data)
        
    def listener_callback(self, msg):
        self.tab=msg.ranges
        self.angle_increment=msg.angle_increment
        self.angle_max=msg.angle_max