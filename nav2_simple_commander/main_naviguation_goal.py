import working_on_foxy as wf
import rclpy

import numpy as np # Scientific computing library for Python
 
def get_quaternion_from_euler(roll, pitch, yaw):
  """
  Convert an Euler angle to a quaternion.
   
  Input
    :param roll: The roll (rotation around x-axis) angle in radians.
    :param pitch: The pitch (rotation around y-axis) angle in radians.
    :param yaw: The yaw (rotation around z-axis) angle in radians.
 
  Output
    :return qx, qy, qz, qw: The orientation in quaternion [x,y,z,w] format
  """
  qx = np.sin(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) - np.cos(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
  qy = np.cos(roll/2) * np.sin(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.cos(pitch/2) * np.sin(yaw/2)
  qz = np.cos(roll/2) * np.cos(pitch/2) * np.sin(yaw/2) - np.sin(roll/2) * np.sin(pitch/2) * np.cos(yaw/2)
  qw = np.cos(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
 
  return [qx, qy, qz, qw]

def main() :
    rclpy.init()
    t=get_quaternion_from_euler(0.0,0.0,0.0)
    qx=t[0]
    qy=t[1]
    qz=t[2]
    qw=t[3]
    
    navigator = wf.BasicNavigatorFoxy()
    security_route = [
            [2.41, 2.28]]
            # [3.08, 2.6],
            # [2.46, -0.564],
            # [1.96, 0.591]]
    navigator.patrol_demo(security_route,quaternion_x=qx, quaternion_y=qy,quaternion_w= qw,quaternion_z= qz)

    exit(0)

if __name__ == '__main__':
    main()