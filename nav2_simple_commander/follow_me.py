
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
import nav2_simple_commander.constants as c
import math
import time
import geometry_msgs.msg
from rclpy.qos import qos_profile_sensor_data



class Recovery_data(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            LaserScan,
            '/scan',
            self.listener_callback,
            qos_profile_sensor_data)
        self.subscription  # prevent unused variable warning
        self.tab=[]
        self.angle=0
        self.angle_max=0
        self.pub = self.create_publisher(
            geometry_msgs.msg.Twist, 'cmd_vel', 10)
        self.x_goal=0
        self.y_goal=0
        
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
        self.get_logger().info('GO TO: "%s"\n' % str(self.x_goal) + " " + str(self.y_goal))
        self.pub.publish(twist)
        
    
    def feet_barrycentre(self):
        #self.get_logger().info('I heard: "%s"\n' % msg.ranges)
        tab_final=[]
        somme_x=0
        somme_y=0
        self.nbre_elt=0
        for i,r in enumerate(self.tab):
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
        self.y_bary=0

    def go_to(self):
        
        if self.nbre_elt == 0:
            self.get_logger().info('aucun elt détecté')
            self.x_goal = 0.0
            self.y_goal =0.0
        else:
            self.x_goal=(self.x_feet-self.x_bary)
            self.y_goal=-(self.y_bary-self.y_feet)
        # if (self.x_goal - x_goal)<1 :
        #     self.x_goal = 0.0
        # if (self.x_goal - x_goal)<1:
        #     self.y_goal=0

        #self.get_logger().info('[x,y]=: "%s"\n' % x_centre + y_centre)

    def emergency_shutdown(self):
        self.get_logger().warn("Emergency shutdown! Spamming a Twist of 0s!")
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

    
    




