#Ce programme permet de suivre une personne avec uniquement quelques points déterminés par le lidar du turtlebot.

from rclpy.node import Node
from sensor_msgs.msg import LaserScan
import nav2_simple_commander.constants as c
import math
import time
import geometry_msgs.msg
from rclpy.qos import qos_profile_sensor_data
import nav2_simple_commander.navigation_goal as ng
import logging

class Recovery_data(Node):
    def __init__(self):
        super().__init__("Follow_me")
        self.log= logging.getLogger('Follow_me')
        self.log.setLevel(c.log_level)
        self.log.info("Début du follow me")
        self.subscription = self.create_subscription(
            LaserScan,
            '/scan',
            self.listener_callback,
            qos_profile_sensor_data)
        self.subscription  # prevent unused variable warning
        self.active = False
        self.tab=[]
        self.angle=0
        self.angle_max=0
        self.pub = self.create_publisher(
            geometry_msgs.msg.Twist, 'cmd_vel', 10)
        self.x_goal=0
        self.y_goal=0
        self.t=time.time()
        self.prev_t=time.time()
        self.tmp=0
        
    def set_active(self, value):
        self.log.debug('Modification de la valeur active par :', value)
        self.active=value
        
    def listener_callback(self, msg):
        if self.active == False: #permet de ne pas lancer le follow me si cette variable est False
            return
        self.tab=msg.ranges
        self.angle_increment=msg.angle_increment
        self.angle_max=msg.angle_max
        #print(self.angle_max)
        self.area_barycentre(c.d_debut,c.d_fin)
        self.feet_barrycentre()
        self.go_to()
        self.set_position()
        #self.get_logger().info('GO TO: x={:1f}"%s"\n' % str(self.x_goal) + " " + str(self.y_goal)) 
        self.afficher_frequence()
    
    def set_position(self):
        twist = geometry_msgs.msg.Twist()
        twist.linear.x = self.x_goal * c.k_linear
        twist.linear.y = 0.0
        twist.linear.z = 0.0
        twist.angular.x = 0.0
        twist.angular.y = 0.0
        twist.angular.z = self.y_goal * c.k_rot
        self.pub.publish(twist)
        
    def afficher_frequence(self):
        self.prev_t=self.t
        self.t=time.time()
        dt=self.t-self.prev_t
        f=0
        if dt!= 0:
            f=1/dt
        self.log.debug('fréquence = {:.1f}Hz'.format(f))
        
    def feet_barrycentre(self):
        #self.get_logger().info('I heard: "%s"\n' % msg.ranges)
        tab_final=[]
        somme_x=0
        somme_y=0
        self.nbre_elt=0
        for i,r in enumerate(self.tab): #pour tous les éléments du tab
            angle=i*self.angle_increment 
            if angle<=c.theta/2 or angle>=(self.angle_max-c.theta/2): 
                if c.d_debut<=r<=c.d_fin:
                    x= r * math.cos(angle)
                    y= r * math.sin(angle)
                    somme_x+=x
                    somme_y+=y
                    self.nbre_elt+=1
        if self.nbre_elt != 0 :
            self.x_feet=somme_x/self.nbre_elt
            self.y_feet=somme_y/self.nbre_elt
        else :
            self.x_feet=self.x_bary
            self.y_feet=self.y_bary
        self.get_logger().info('feet: "%s"\n' % str(self.x_feet) + " " + str(self.y_feet))
        
    def area_barycentre(self, d_debut,d_fin):
        self.x_bary=(d_debut+d_fin)/2
        self.y_bary=0.0

    def go_to(self):
        if self.nbre_elt == 0: #si pas d'élements détectés
            print("aucun élement n'est détecté\n")
            self.x_goal = 0.0
            self.y_goal =0.0
        else:
            self.x_goal=(self.x_feet-self.x_bary)
            self.y_goal=-(self.y_bary-self.y_feet)
            print("stop timer= ", self.tmp)
            if self.x_goal < c.diff_bary_feet and self.y_goal < c.diff_bary_feet: #si les barycentres sont toujours égaux
                print("pas de mvt détectée")
                self.tmp+=1
                self.stop_move()
                if self.tmp == c.stop_timer: #si trop de temps attendus on sort du follow_me
                    self.stop_move()
                    self.tmp=0
                    print("4s sans detection \n")   
                    self.set_active(False)
                    return
            else :
                self.tmp=0
                
    def stop_move(self):
        twist = geometry_msgs.msg.Twist()
        twist.linear.x = 0.0
        twist.linear.y = 0.0
        twist.linear.z = 0.0
        twist.angular.x = 0.0
        twist.angular.y = 0.0
        twist.angular.z = 0.0
        self.pub.publish(twist)

    def stop_follow_me(self):
        self.get_logger().warn("Arrêt du follow_me\n")
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