
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
import constants as c
import math
import time
import geometry_msgs.msg



class Recovery_data(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            LaserScan,
            'scan',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning
        self.tab=[]
        self.angle=0
        self.angle_max=0
        self.pub = self.create_publisher(
            geometry_msgs.msg.Twist, 'cmd_vel', 10)
        
    def listener_callback(self, msg):
        #self.get_logger().info('I heard: "%s"\n' % msg.ranges)
        #self.get_logger().info('I heard: "%s"\n' % msg.angle_max)
        self.tab=msg.ranges
        self.angle_increment=msg.angle_increment
        self.angle_max=msg.angle_max
        #print(self.angle_max)
        self.area_barycentre(c.d_debut,c.d_fin)
        self.feet_barrycentre()
        self.go_to()
        twist = geometry_msgs.msg.Twist()
        twist.linear.x = self.x_goal * c.k_linear
        twist.linear.y = 0.0
        twist.linear.z = 0.0
        twist.angular.x = 0.0
        twist.angular.y = 0.0
        twist.angular.z = self.y_goal * c.k_rot
        self.pub.publish(twist)
        #self.get_logger().info('GO TO: "%s"\n' % str(self.x_goal) + " " + str(self.y_goal))
    
    def feet_barrycentre(self):
        #self.get_logger().info('I heard: "%s"\n' % msg.ranges)
        tab_final=[]
        somme_x=0
        somme_y=0
        nbre_elt=0
        for i,r in enumerate(self.tab):
            angle=i*self.angle_increment 
            if angle<=c.theta/2 or angle>=(self.angle_max-c.theta/2):
                if c.d_debut<=r<=c.d_fin:
                    x= r * math.cos(angle)
                    y= r * math.sin(angle)
                    somme_x+=x
                    somme_y+=y
                    nbre_elt+=1
        self.x_feet=somme_x/nbre_elt
        self.y_feet=somme_y/nbre_elt
    
    def area_barycentre(self, d_debut,d_fin):
        self.x_bary=(d_debut+d_fin)/2
        self.y_bary=0

    def go_to(self):
        self.x_goal=self.x_feet-self.x_bary
        self.y_goal=self.y_feet-self.y_bary
        #self.get_logger().info('[x,y]=: "%s"\n' % x_centre + y_centre)

    
    




