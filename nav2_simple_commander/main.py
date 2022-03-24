import nav2_simple_commander.navigation_goal as ng
import math
import rclpy
import recovery_data_lidar as rdl
import constants as c
#import follow_me as fm


def main():
    
    rclpy.init()
    
    #nav_goal
    #donner position en x,y, theta 
    #ng.navigation_goal(x=2.41,y=2.28,theta=math.pi)

    #follow_me
    rd = rdl.Recovery_data()
    rclpy.spin(rd)
    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    rd.destroy_node()
    rclpy.shutdown()

    exit(0)

if __name__ == '__main__':
    main()