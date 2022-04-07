import sys

from matplotlib import scale
import os

import geometry_msgs.msg
import rclpy

from rclpy.node import Node
import pygame
import time
import math
import numpy as np
import traceback
import sys
from rclpy.qos import ReliabilityPolicy, QoSProfile
import nav2_simple_commander.follow_me as fm
import nav2_simple_commander.constants as c


msg = """
This node takes inputs from a controller and publishes them
as Twist messages. Tested on a SONY Dual shock 4 controller.

Left joy: holonomic translations
Right joy: rotation 

L2/L1 : increase/decrease only linear speed by 5% (additive)
R2/R1 : increase/decrease only angular speed by 5% (additive)

CTRL-C  or press CIRCLE on the controller to quit
"""

# Button  0 = X / A
# Button  1 = O / B
# Button  2 = Triangle
# Button  3 = Square / X
# Button  4 = l1 / Y
# Button  5 = r1
# Button  6 = l2 / LB
# Button  7 = r2 / RB
# Button  8 = share
# Button  9 = options
# Button 10 = ps_button
# Button 11 = joy_left /start
# Button 12 = joy_right


def sign(x):
    if x >= 0:
        return 1
    else:
        return -1


class JoyTeleop(Node):
    def __init__(self, follow_me_node,recup_pos_node, nav_goal_node):
        super().__init__('Manette')
        self.get_logger().info("Début du programme avec la manette!")
        pygame.init()
        pygame.joystick.init()
        self.nb_joy = pygame.joystick.get_count()
        if self.nb_joy < 1:
            self.get_logger().error("Pas de manette detectée.")
            self.emergency_shutdown()
        self.get_logger().info("nb joysticks: {}".format(self.nb_joy))
        self.j = pygame.joystick.Joystick(0)
        self.nb_hat = self.j.get_numhats()
        self.lin_speed_ratio = 0.2
        self.rot_speed_ratio = 0.9
        # The joyticks dont come back at a perfect 0 position when released. Any abs(value) below min_joy_position will be assumed to be 0
        self.min_joy_position = 0.2
        self.pub = self.create_publisher(
            geometry_msgs.msg.Twist, 'cmd_vel', 10)
        self.create_timer(0.01, self.main_tick)
        self.get_logger().info(msg)
        self.follow_me_node = follow_me_node
        self.recup_pos_node = recup_pos_node
        self.nav_goal_node = nav_goal_node
        self.t=time.time()
        self.prev_t=time.time()
        self.tmp=0
        self.active_fm=False
        self.active_ng=False
        

    def emergency_shutdown(self):
        self.get_logger().warn("Arrêt d'urgence du robot!")
        while True:
            twist = geometry_msgs.msg.Twist()
            twist.linear.x = 0.0
            twist.linear.y = 0.0
            twist.linear.z = 0.0
            twist.angular.x = 0.0
            twist.angular.y = 0.0
            twist.angular.z = 0.0
            self.pub.publish(twist)
            time.sleep(0.01)

    def tick_controller(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.emergency_shutdown()
            elif event.type == pygame.JOYBUTTONDOWN:
                if self.j.get_button(1):
                    self.get_logger().warn("Pressed emergency stop!")
                    self.emergency_shutdown()
                if self.j.get_button(7):
                    self.mode_exam()
            elif event.type == pygame.JOYHATMOTION:
                if self.j.get_hat(0)==(0, 1): # fleche haut    
                    self.lin_speed_ratio = min(1.0, self.lin_speed_ratio+0.05)
                    self.get_logger().info("max translational speed: {:.1f}%, max rotational speed: {:.1f}%".format(
                        self.lin_speed_ratio*100, self.rot_speed_ratio*100))
                if self.j.get_hat(0)==(1, 0):  # fleche droite
                    self.rot_speed_ratio = min(1.0, self.rot_speed_ratio+0.05)
                    self.get_logger().info("max translational speed: {:.1f}%, max rotational speed: {:.1f}%".format(
                        self.lin_speed_ratio*100, self.rot_speed_ratio*100))
                if self.j.get_hat(0)== (0, -1):  # fleche gauche
                    self.lin_speed_ratio = max(0.0, self.lin_speed_ratio-0.05)
                    self.get_logger().info("max translational speed: {:.1f}%, max rotational speed: {:.1f}%".format(
                        self.lin_speed_ratio*100, self.rot_speed_ratio*100))
                if self.j.get_hat(0)==(-1, 0):  # fleche bas
                    self.rot_speed_ratio = max(0.0, self.rot_speed_ratio-0.05)
                    self.get_logger().info("max translational speed: {:.1f}%, max rotational speed: {:.1f}%".format(
                        self.lin_speed_ratio*100, self.rot_speed_ratio*100))
            elif event.type == pygame.JOYAXISMOTION:
                    if self.j.get_axis(4)>0:
                        self.follow_me_node.active = True
                        os.system("cd Desktop/sons\ turtlpute/ && play FOLLOW_MEEEEE.wav")
                    if self.j.get_axis(5)>0:
                        self.follow_me_node.active = False
            else:
                pass

        if self.nb_joy != pygame.joystick.get_count():
            self.get_logger().warn("Manette déconnectée")
            self.emergency_shutdown()
            
    def mode_exam(self):
        self.get_logger().info("Début du mode examen")
        while (not self.active_fm and not self.active_ng):
            if not self.active_fm :
                self.follow_me_node.active =True
                self.active_fm = True
            if self.active_fm and not self.active_ng:
                self.nav_goal_node.active = True
                #self.get_logger().info("x= " + str(self.recup_pos_node.get_x()) + " y= " + str(self.recup_pos_node.get_y()))
                self.active_ng = True
        

    def rumble(self, duration):
        self.rumble_start = time.time()
        self.is_rumble = True
        self.rumble_duration = duration
        # Duration doesn't work, have to do it ourselves
        self.j.rumble(1, 1, 1000)

    def print_controller(self):
        # Get the name from the OS for the controller/joystick.
        #time.sleep(1)
        name = self.j.get_name()
        self.get_logger().info("Joystick name: {}".format(name))

        # Usually axis run in pairs, up/down for one, and left/right for
        # the other.
        axes = self.j.get_numaxes()
        self.get_logger().info("Number of axes: {}".format(axes))
        self.get_logger().info("nb hat : {}".format(self.nb_hat))
        hats = self.j.get_hat(0)
        self.get_logger().info("current hat : {}".format(hats))
        for i in range(axes):
            axis = self.j.get_axis(i)
            self.get_logger().info("Axis {} value: {:>6.3f}".format(i, axis))

        buttons = self.j.get_numbuttons()
        self.get_logger().info("Number of buttons: {}".format(buttons))

        for i in range(buttons):
            button = self.j.get_button(i)
            self.get_logger().info("Button {:>2} value: {}".format(i, button))

    def speeds_from_joystick(self):
        cycle_max_t = self.lin_speed_ratio  # 0.2*factor
        cycle_max_r = self.rot_speed_ratio  # 0.1*factor

        if abs(self.j.get_axis(1)) < self.min_joy_position:
            x = 0.0
        else:
            x = (-self.j.get_axis(1) * cycle_max_t)/5

        if abs(self.j.get_axis(0)) < self.min_joy_position:
            y = 0.0
        else:
            y = -self.j.get_axis(0) * cycle_max_t

        if abs(self.j.get_axis(2)) < self.min_joy_position:
            rot = 0.0
        else:
            rot = -self.j.get_axis(2) * cycle_max_r

        return x, y, rot

    def main_tick(self):
        self.tick_controller()
        if not self.follow_me_node.active and not self.nav_goal_node.active and not self.recup_pos_node.activate:
            x, y, theta = self.speeds_from_joystick()
            twist = geometry_msgs.msg.Twist()
            twist.linear.x = x
            twist.linear.y = y
            twist.linear.z = 0.0
            twist.angular.x = 0.0
            twist.angular.y = 0.0
            twist.angular.z = theta
            self.pub.publish(twist)
            self.prev_t = time.time()
            self.get_logger().info("\nx_vel: {:.1f}%, y_vel: {:.1f}%, theta_vel: {:.1f}%.\nMax lin_vel: {:.1f}%, max rot_vel: {:.1f}%".format(
             x*100, y*100, theta*100, self.lin_speed_ratio*100, self.rot_speed_ratio*100))
            # self.prev_t=self.t
            # self.t=time.time()
            # dt=self.t-self.prev_t
            # f=0
            # if dt!= 0: theta
        else:
            x, y, theta = -0.01,-0.01,-0.01
        
        self.get_logger().info(" Follow me : {}".format(self.follow_me_node.active))
            #self.print_controller()


# def main():
#     rclpy.init()
#     node_2 = fm.Recovery_data()
#     node = JoyTeleop(node_2)
    # rclpy.init()
#         #rclpy.spin(node)
#     except Exception as e:
#         traceback.print_exc()
#     finally:
#         node.emergency_shutdown()
#         node.destroy_node()
#         rclpy.shutdown()
    



# if __name__ == '__main__':
#     main()
    # rclpy.init()