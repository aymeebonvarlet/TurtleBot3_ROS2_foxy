
from turtle import delay

#from black import T
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
import nav2_simple_commander.constants as c
import math
import time
import geometry_msgs.msg
from rclpy.qos import qos_profile_sensor_data
import nav2_simple_commander.navigation_goal as ng



class Recovery_data(Node):
    def __init__(self):
        super().__init__('minimal_subscriber')
        print("Début du follow me")
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
        
    def listener_callback(self, msg):
        if self.active == False:
            return
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
        self.prev_t=self.t
        self.t=time.time()
        dt=self.t-self.prev_t
        f=0
        if dt!= 0:
            f=1/dt
        self.get_logger().info('fréquence = {:.1f}Hz'.format(f) )
        
        
    
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
        self.y_bary=0.0

    def go_to(self):
        if self.nbre_elt == 0:
            print("aucun élement n'est détecté\n")
            self.x_goal = 0.0
            self.y_goal =0.0
        else:
            self.x_goal=(self.x_feet-self.x_bary)
            self.y_goal=-(self.y_bary-self.y_feet)
            # tmp=0
            # while(self.x_goal ==0.0 and self.y_goal==0.0):
            #     tmp+=1
            #     delay(1000)
            #     if tmp == 10:
            #         self.stop_follow_me()
            #         #ng.navigation_goal(x=c.x_retour,y=c.x_retour,theta=c.theta_retour)
                
        


    def stop_follow_me(self):
        self.get_logger().warn("Arrêt du follow_me\n")
        while True:
            twist = geometry_msgs.msg.Twist()
            twist.linear.x = 0.0
            self.x_goal=(self.x_feet-self.x_bary)
            self.y_goal=-(self.y_bary-self.y_feet)
            twist.linear.y = 0.0
            twist.linear.z = 0.0
            twist.angular.x = 0.0
            twist.angular.y = 0.0
            twist.angular.z = 0.0
            self.pub.publish(twist)
            time.sleep(0.01)

    
    




