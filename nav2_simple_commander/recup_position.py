from rclpy.node import Node
import nav2_simple_commander.constants as c
from geometry_msgs.msg import PoseWithCovarianceStamped
from rclpy.qos import qos_profile_sensor_data
import nav2_simple_commander.navigation_goal as ng
import logging

class Recup_pos(Node):
    def __init__(self):
        super().__init__("Recup_position")
        self.log=self.get_logger()
        self.log.set_level(c.log_level)
        self.log.info("Initialisation de la classe Recup_pos")
        self.sub = self.create_subscription(
            PoseWithCovarianceStamped,
            '/amcl_pose',
            self._callback,
            qos_profile_sensor_data)
        self.sub
        self.activate = False
        self.log.debug("fin")
        
    def _callback(self, msg):
        self.log.debug("dans recup pos")
        if not self.activate:
            return 
        self.position=msg.pose.pose.position
        self.x= self.position.x
        self.y= self.position.y
        self.orientation=msg.pose.pose.orientation
        self.qz= self.orientation.z
        self.qw= self.orientation.w
        self.log.debug("x= " + str(self.x) + '\n')
        self.log.debug("y= " + str(self.y) + '\n')
        self.log.debug("qz= " + str(self.qz) + '\n')
        self.log.debug("qw= " + str(self.qw) + '\n')
    
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    
    def get_qz(self):
        return self.qz
    
    def get_qw(self):
        return self.qw
    
        # self.angle_increment=msg.angle_increment
        # self.angle_max=msg.angle_max
        
        
    #     geometry_msgs.msg.PoseWithCovariance(pose=geometry_msgs.msg.Pose(position=geometry_msgs.msg.Point(x=1.4410737722134768, y=1.1381386830536893, z=0.0), orientation=geometry_msgs.msg.Quaternion(x=0.0, y=0.0, z=0.4240722794545024, w=0.9056283463972749)), covariance=array([0.04145631, 0.00751765, 0.        , 0.        , 0.        ,
    #    0.        , 0.00751765, 0.01890331, 0.        , 0.        ,
    #    0.        , 0.        , 0.        , 0.        , 0.        ,
    #    0.        , 0.        , 0.        , 0.        , 0.        ,
    #    0.        , 0.        , 0.        , 0.        , 0.        ,
    #    0.        , 0.        , 0.        , 0.        , 0.        ,
    #    0.        , 0.        , 0.        , 0.        , 0.        ,
    #    0.05607393]))
