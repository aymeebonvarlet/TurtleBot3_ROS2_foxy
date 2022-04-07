#import nav2_simple_commander.navigation_goal as ng
from nav2_simple_commander.controller import JoyTeleop
import nav2_simple_commander.navigation_goal as ng
import rclpy
import nav2_simple_commander.follow_me as fm
import nav2_simple_commander.constants as c
import nav2_simple_commander.controller as controller
import nav2_simple_commander.recup_position as rp

import traceback
from rclpy.node import Node
import math

#import follow_me as fm


def main():
    
    rclpy.init()
    
    #nav_goal
    #donner position en x,y, theta 
    # nav_goal = ng.Navigation_goal()
    # nav_goal.navigation_goal(x=0.5,y=1.0,theta=math.pi)

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
        
    # #controller
    # follow_me = fm.Recovery_data()
    # nav_goal = ng.Navigation_goal()
    # recup_pos=rp.Initial_position()
    # control=controller.JoyTeleop(follow_me)
    # try:
    #     while(True):
    #         rclpy.spin_once(follow_me)
    #         rclpy.spin_once(control)
    # except Exception as e:
    #     traceback.print_exc()
    # finally:
    #     follow_me.stop_follow_me()
    #     follow_me.destroy_node()
    #     rclpy.shutdown    
    
    #recup position
    # recup_pos=rp.Initial_position()
    # try:
    #     rclpy.spin_once(recup_pos)
    # except Exception as e:
    #     traceback.print_exc()
    # finally:
    #     rclpy.shutdown()
    

    exit(0)

if __name__ == '__main__':
    main()