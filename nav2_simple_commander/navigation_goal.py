import nav2_simple_commander.working_on_foxy as wf
import numpy as np # Scientific computing library for Python
from rclpy.node import Node
import nav2_simple_commander.constants as c 

class Navigation_goal(Node):
  def __init__(self):
    super().__init__('Navigation_goal')
    self.log=self.get_logger()
    self.log.set_level(c.log_level)
  
  def _get_quaternion_from_euler(self,roll, pitch, yaw):
    """
  Convert an Euler angle to a quaternion.
   
  Input
    :param roll: The roll (rotation around x-axis) angle in radians.
    :param pitch: The pitch (rotation around y-axis) angle in radians.
    :param yaw: The yaw (rotation around z-axis) angle in radians.
 
  Output
    :return qx, qy, qz, qw: The orientation in quaternion [x,y,z,w] format
  """
    self.qx = np.sin(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) - np.cos(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
    self.qy = np.cos(roll/2) * np.sin(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.cos(pitch/2) * np.sin(yaw/2)
    self.qz = np.cos(roll/2) * np.cos(pitch/2) * np.sin(yaw/2) - np.sin(roll/2) * np.sin(pitch/2) * np.cos(yaw/2)
    self.qw = np.cos(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
  
    

  def navigation_goal(self, x,y,theta):
    self.log.info("Début du navigation goal\n")
    #On tourne que sur l'axe yaw, donc roll=pitch=0.0
    self._get_quaternion_from_euler(roll=0.0,pitch=0.0,yaw=theta)
    navigator = wf.BasicNavigatorFoxy()
    navigator.applicate_coor(coor=[x,y],quaternion_x=self.qx, quaternion_y=self.qy, quaternion_w=self.qw,quaternion_z=self.qz)
    self.log.info("Nous sommes arrivés à destination\n")