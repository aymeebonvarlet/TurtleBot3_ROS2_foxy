import sys

from matplotlib import scale
import os

import geometry_msgs.msg
import rclpy

from rclpy.node import Node
import pygame
import time
import numpy as np
import sys
from rclpy.qos import ReliabilityPolicy, QoSProfile
import nav2_simple_commander.follow_me as fm
import nav2_simple_commander.constants as c
import nav2_simple_commander.exam as exam 


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
    def __init__(self, follow_me_node):
        super().__init__('Manette')
        self.log=self.get_logger()
        self.log.set_level(c.log_level)
        self.log.info("Début du programme avec la manette!")
        pygame.init()
        pygame.joystick.init()
        self.nb_joy = pygame.joystick.get_count()
        if self.nb_joy < 1:
            self.log.error("Pas de manette detectée.")
            self.emergency_shutdown()
        self.log.debug("nb joysticks: {}".format(self.nb_joy))
        self.j = pygame.joystick.Joystick(0)
        self.nb_hat = self.j.get_numhats()
        self.lin_speed_ratio = c.k_linear_controller
        self.rot_speed_ratio = c.k_rot_controller
        # The joyticks dont come back at a perfect 0 position when released. Any abs(value) below min_joy_position will be assumed to be 0
        self.min_joy_position = 0.2
        self.pub = self.create_publisher(
            geometry_msgs.msg.Twist, 'cmd_vel', 10)
        self.create_timer(0.01, self.main_tick)
        self.get_logger().info(msg)
        self.follow_me_node = follow_me_node
        self.t=time.time()
        self.prev_t=time.time()
        self.tmp=0

    def emergency_shutdown(self):
        self.log.debug("Arrêt d'urgence du robot!")
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
                    self.log.warning("Pressed emergency stop!")
                    self.emergency_shutdown()
                if self.j.get_button(7):
                    examen = exam.Exam()
            elif event.type == pygame.JOYHATMOTION:
                if self.j.get_hat(0)==(0, 1): # fleche haut    
                    self.lin_speed_ratio = min(1.0, self.lin_speed_ratio+0.05)
                    self.log.debug("max translational speed: {:.1f}%, max rotational speed: {:.1f}%".format(
                        self.lin_speed_ratio*100, self.rot_speed_ratio*100))
                if self.j.get_hat(0)==(1, 0):  # fleche droite
                    self.rot_speed_ratio = min(1.0, self.rot_speed_ratio+0.05)
                    self.log.debug("max translational speed: {:.1f}%, max rotational speed: {:.1f}%".format(
                        self.lin_speed_ratio*100, self.rot_speed_ratio*100))
                if self.j.get_hat(0)== (0, -1):  # fleche gauche
                    self.lin_speed_ratio = max(0.0, self.lin_speed_ratio-0.05)
                    self.log.debug("max translational speed: {:.1f}%, max rotational speed: {:.1f}%".format(
                        self.lin_speed_ratio*100, self.rot_speed_ratio*100))
                if self.j.get_hat(0)==(-1, 0):  # fleche bas
                    self.rot_speed_ratio = max(0.0, self.rot_speed_ratio-0.05)
                    self.log.debug("max translational speed: {:.1f}%, max rotational speed: {:.1f}%".format(
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
            self.log.warning("Manette déconnectée")
            self.emergency_shutdown()

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
        self.log.debug("Joystick name: {}".format(name))

        # Usually axis run in pairs, up/down for one, and left/right for
        # the other.
        axes = self.j.get_numaxes()
        self.log.debug("Number of axes: {}".format(axes))
        self.log.debug("nb hat : {}".format(self.nb_hat))
        hats = self.j.get_hat(0)
        self.log.debug("current hat : {}".format(hats))
        for i in range(axes):
            axis = self.j.get_axis(i)
            self.log.debug("Axis {} value: {:>6.3f}".format(i, axis))

        buttons = self.j.get_numbuttons()
        self.log.debug("Number of buttons: {}".format(buttons))

        for i in range(buttons):
            button = self.j.get_button(i)
            self.log.debug("Button {:>2} value: {}".format(i, button))

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
        if self.follow_me_node.active == False:
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
            self.prev_t=self.t
            self.t=time.time()
            dt=self.t-self.prev_t
            f=0
            if dt!= 0: 
                f=1/dt
            self.log.debug('fréquence = {:.1f}Hz'.format(f) )
        else:
            x, y, theta = -0.01,-0.01,-0.01
        
        self.log.debug(" Follow me : {}".format(self.follow_me_node.active))
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