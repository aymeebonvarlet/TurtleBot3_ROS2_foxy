#import nav2_simple_commander.navigation_goal as ng
import math
import rclpy
import nav2_simple_commander.follow_me as rdl
import nav2_simple_commander.constants as c
import traceback
from rclpy.node import Node

#import follow_me as fm


def main():
    
    rclpy.init()
    
    #nav_goal
    #donner position en x,y, theta 
    #ng.navigation_goal(x=2.41,y=2.28,theta=math.pi)

    #follow_me
    rd = rdl.Recovery_data()
    try:
        rclpy.spin(rd)
    except Exception as e:
        traceback.print_exc()
    finally:
        rd.emergency_shutdown()
        rd.destroy_node()
        rclpy.shutdown()
    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    

    exit(0)

if __name__ == '__main__':
    main()