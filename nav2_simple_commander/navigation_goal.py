import nav2_simple_commander.working_on_foxy as wf


import numpy as np # Scientific computing library for Python
 
 #fonction qui permet d'obtenir les valeurs quaternion pour la rotation
def _get_quaternion_from_euler(roll, pitch, yaw):
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

def navigation_goal(x,y,theta):
    print("Début du navigation goal\n")
    #On tourne que sur l'axe yaw, donc roll=pitch=0.0
    t=_get_quaternion_from_euler(roll=0.0,pitch=0.0,yaw=theta)
    qx=t[0]
    qy=t[1]
    qz=t[2]
    qw=t[3]
    
    navigator = wf.BasicNavigatorFoxy()
    navigator.applicate_coor(coor=[x,y],quaternion_x=qx, quaternion_y=qy, quaternion_w=qw,quaternion_z=qz)
    print("Nous sommes arrivés à destination\n")