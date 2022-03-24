#import nav2_simple_commander.navigation_goal as ng
import math
import rclpy
import nav2_simple_commander.follow_me as fm
import nav2_simple_commander.constants as c
import nav2_simple_commander.navigation_goal as ng
import traceback
from rclpy.node import Node

#import follow_me as fm


def main():
    
    rclpy.init()
    
    #nav_goal
    #donner position en x,y, theta 
    #ng.navigation_goal(x=1.88,y=0.882,theta=math.pi)

    #follow_me
    fm = fm.Recovery_data()
    try:
        rclpy.spin(fm)
    except Exception as e:
        traceback.print_exc()
    finally:
        fm.emergency_shutdown()
        fm.destroy_node()
        rclpy.shutdown()
    

    exit(0)

if __name__ == '__main__':
    main()