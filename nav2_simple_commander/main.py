import nav2_simple_commander.navigation_goal as ng
import math
import rclpy


def main():
    
    rclpy.init()
    
    ng.navigation_goal(x=2.41,y=2.28,theta=math.pi)

    exit(0)

if __name__ == '__main__':
    main()