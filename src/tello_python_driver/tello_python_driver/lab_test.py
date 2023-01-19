import rclpy
from rclpy.node import Node

from std_msgs.msg import String

import time
from std_msgs.msg import *
from geometry_msgs.msg import Twist, Pose
from nav_msgs.msg import Odometry
import time
import numpy as np
import pygame


class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.subscription = self.create_subscription(
            Pose,
            'optitrack_topic',
            self.listener_callback,
            10)
        self.publisher_parameters = self.create_publisher(Twist, '/cmd_vel', 10)


        self.parameters = Twist()

        #self.vx = self.vy = self.vz = self.ax = self.ay = self.az = 0.0
        self.x = self.y = self.z = self.alfa = self.betta = self.gamma = 0.0
        self.dest_x = 0.0
        self.dest_y = 0.0
        self.dest_z = 1.0
        self.Data = np.genfromtxt("traj_adele.txt", dtype=float,
                        encoding=None, delimiter=",")
        self.num_lines = 0
        with open(r"traj_adele.txt", 'r') as fp:
            self.num_lines = len(fp.readlines())
        timer_period = self.Data[self.num_lines-1][0]/self.num_lines  # seconds
        print(timer_period)
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0
        print("Let's go 😎️🤯️😵️")
        pygame.mixer.init()
        pygame.mixer.music.load("Adele.mp3")
        pygame.mixer.music.play()

    def listener_callback(self, msg):
        
        self.x = msg.position.x
        self.y = msg.position.y
        self.z = msg.position.z
        if abs(self.dest_x - self.x) > 0.1 or abs(self.dest_y - self.y) > 0.1 or abs(self.dest_z - self.z) > 0.1:
            self.parameters.linear.x = (self.dest_x - self.x)
            self.parameters.linear.y = (self.dest_y - self.y) 
            self.parameters.linear.z = (self.dest_z - self.z) 
            if self.parameters.linear.x > 0.3:
                self.parameters.linear.x =  0.3
            if self.parameters.linear.y > 0.3:
                self.parameters.linear.y =  0.3
            if self.parameters.linear.z >0.4:
                self.parameters.linear.z = 0.4
            if self.parameters.linear.x < - 0.3:
                self.parameters.linear.x = - 0.3
            if self.parameters.linear.y < - 0.3:
                self.parameters.linear.y = - 0.3
            if self.parameters.linear.z < -0.4:
                self.parameters.linear.z = -0.4
                
            if self.parameters.linear.x <0.1 and self.parameters.linear.x >-0.1 :
                self.parameters.linear.x = 0.0
            if self.parameters.linear.y <0.1 and self.parameters.linear.y >-0.1 :
                self.parameters.linear.y = 0.0
            if self.parameters.linear.z <0.1 and self.parameters.linear.z >-0.1 :
                self.parameters.linear.z = 0.0

            self.publisher_parameters.publish(self.parameters)
            print('goTo x=' + str(round(self.x, 3)) + '; y=' + str(round(self.y, 3)) + '; z=' + str(round(self.z, 3)))
            #time.sleep(0.1)
        else:
            self.clear()
            self.publisher_parameters.publish(self.parameters)

            time.sleep(0.1)
            
    def clear(self):
        self.parameters.linear.x = 0.0
        self.parameters.linear.y = 0.0
        self.parameters.linear.z = 0.0
        self.parameters.angular.x = 0.0
        self.parameters.angular.y = 0.0
        self.parameters.angular.z = 0.0
        
    def timer_callback(self):
        if self.i < self.num_lines - 1:
            print('********************')
            print('New data',self.Data[self.i])
            print('********************')
            self.dest_x=self.Data[self.i][1]
            self.dest_y=self.Data[self.i][2]
            self.dest_z=self.Data[self.i][3]
            self.i=self.i+1
            
            if self.dest_x < -1:
                self.dest_x = -1
            if self.dest_x > 1:
                self.dest_x = 1
            
            if self.dest_y < -1:
                self.dest_y = -1
            if self.dest_y > 1:
                self.dest_y = 1
            
            if self.dest_z < 0.3:
                self.dest_z = 0.3
            if self.dest_z > 1.7:
                self.dest_z = 1.7    
            
        else:
            print("********NO NEW DATA********")


def main(args=None):
    print("#######################################################")
    rclpy.init(args=args)
    minimal_publisher = MinimalPublisher()
    rclpy.spin(minimal_publisher)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
