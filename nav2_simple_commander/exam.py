from rclpy.node import Node
import nav2_simple_commander.constants as c
import math
import time
import geometry_msgs.msg
from rclpy.qos import qos_profile_sensor_data
import nav2_simple_commander.navigation_goal as ng
import nav2_simple_commander.follow_me as fm
import nav2_simple_commander.recup_position as rp




class Exam(Node):
    def __init__(self, follow_me_node, recup_pos_node, nav_goal_node):
        super().__init__("Mode_examen")
        self.log=self.get_logger()
        self.log.set_level(c.log_level)
        self.log.info("Mode examen activé")
        self.follow_me_node = follow_me_node
        self.recup_pos_node = recup_pos_node
        self.nav_goal_node = nav_goal_node
    
    def go(self):
        navigation_goal = ng.Navigation_goal()
        follow_me = fm.Recovery_data()
        recup_pos = rp.Initial_position()
        
        