#import nav2_simple_commander.navigation_goal as ng
import math
from nav2_simple_commander.controller import JoyTeleop
import rclpy
import nav2_simple_commander.follow_me as fm
import nav2_simple_commander.constants as c
import nav2_simple_commander.controller as controller

import traceback
from rclpy.node import Node

#import follow_me as fm


def main():
    
    rclpy.init()
    
    #nav_goal
    #donner position en x,y, theta 
    #ng.navigation_goal(x=1.88,y=0.882,theta=math.pi)

    #follow_me
    # follow_me = fm.Recovery_data()
    # try:
    #     rclpy.spin(follow_me)
    # except Exception as e:
    #     traceback.print_exc()
    # finally:
    #     follow_me.stop_follow_me()
    #     follow_me.destroy_node()
    #     rclpy.shutdown()
        
    #controller
    follow_me = fm.Recovery_data()
    control=controller.JoyTeleop(follow_me)
    try:
        while(True):
            rclpy.spin_once(follow_me)
            rclpy.spin_once(control)
    except Exception as e:
        traceback.print_exc()
    finally:
        follow_me.stop_follow_me()
        follow_me.destroy_node()
        rclpy.shutdown    
    

    exit(0)

if __name__ == '__main__':
    main()