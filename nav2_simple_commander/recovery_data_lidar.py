
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
import constants as c
import math



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
        
    def listener_callback(self, msg):
        #self.get_logger().info('I heard: "%s"\n' % msg.ranges)
        #self.get_logger().info('I heard: "%s"\n' % msg.angle_max)
        self.tab=msg.ranges
        self.angle_increment=msg.angle_increment
        self.angle_max=msg.angle_max
        #print(self.angle_max)
        print("x,y=",self.go_to_barrycentre)
    
    def go_to_barrycentre(self):
        #self.get_logger().info('I heard: "%s"\n' % msg.ranges)
        tab_final=[]
        somme_x=0
        somme_y=0
        nbre_elt=0
        for i,r in enumerate(self.tab):
            #print("c.theta=",c.theta, "i= ", i*self.angle, "c.d_debut", c.d_debut, "c.dfin= ", c.d_fin, self.tab[i])
            angle=i*self.angle_increment #en rad
            #print("r=", r, "angle= ", angle)
            if angle<=c.theta/2 or angle>=(self.angle_max-c.theta/2):
                if c.d_debut<=r<=c.d_fin:
                    x= r * math.cos(angle)
                    y= r * math.sin(angle)
                    somme_x+=x
                    somme_y+=y
                    nbre_elt+=1
        x_final=somme_x/nbre_elt
        y_final=somme_y/nbre_elt
        return [x_final, y_final]




