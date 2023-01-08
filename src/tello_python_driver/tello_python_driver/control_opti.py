
            
import rclpy
from rclpy.node import Node

from std_msgs.msg import String

import time
from std_msgs.msg import *
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import time
import numpy as np
# from ardrone_autonomy.msg import Navdata # for receiving navdata feedback


c_max_critical_time = 3
c_min_critical_time = 0.2




def handler(event, sender, data, **args):
    global prev_flight_data
    drone = sender
    if event is drone.EVENT_CONNECTED:
        print('connected')
        drone.start_video()
        drone.set_exposure(0)
        drone.set_video_encoder_rate(4)
    elif event is drone.EVENT_FLIGHT_DATA:
        if prev_flight_data != str(data):
            print(data)
            prev_flight_data = str(data)


class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        self.subscription = self.create_subscription(Odometry, '/repeater/tello_1/pose/info', self.listener_callback, 10)
        self.publisher_parameters = self.create_publisher(Twist, '/cmd_vel', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0
        self.status = -1
        self.parameters = Twist()
        self.speed = 0.4
        self.airborne = False
        self.max_critical_time = 3  # sec
        self.min_critical_time = 0.2  # sec
        self.vx = self.vy = self.vz = self.ax = self.ay = self.az = 0.0
        self.x = self.y = self.z = self.alfa = self.betta = self.gamma = 0.0

        self.last_time = None
        self.dt = 0.0
    def goTo(self, x, y, z, dt=0.5):
        self.clear()
        x = float(x)
        y = float(y)
        z = float(z)
        self.clear()
        self.publisher_parameters.publish(self.parameters)
        while abs(x - self.x) > 0.05 or abs(y - self.y) > 0.05 or abs(z - self.z) > 0.05:
            self.parameters.linear.x = (x - self.x)
            self.parameters.linear.y = (y - self.y) 
            self.parameters.linear.z = -(z - self.z) 
            if self.parameters.linear.x >0.2:
                self.parameters.linear.x = 0.2
            if self.parameters.linear.y >0.2:
                self.parameters.linear.y = 0.2
            if self.parameters.linear.z >0.2:
                self.parameters.linear.z = 0.2
            if self.parameters.linear.x < -0.2:
                self.parameters.linear.x = -0.2
            if self.parameters.linear.y < -0.2:
                self.parameters.linear.y = -0.2
            if self.parameters.linear.z < -0.2:
                self.parameters.linear.z = -0.2
                
            if self.parameters.linear.x <0.05 and self.parameters.linear.x >-0.05 :
                self.parameters.linear.x = 0.0
            if self.parameters.linear.y <0.05 and self.parameters.linear.y >-0.05 :
                self.parameters.linear.y = 0.0
            if self.parameters.linear.z <0.05 and self.parameters.linear.z >-0.05 :
                self.parameters.linear.z = 0.0

            
            print('********************')
            print(self.parameters.linear.x)
            print(self.parameters.linear.y)
            print(self.parameters.linear.z)
            print('********************')
            
            self.publisher_parameters.publish(self.parameters)
            self.x = self.x + self.parameters.linear.x*dt
            self.y = self.y + self.parameters.linear.y*dt
            self.z = (self.z + self.parameters.linear.z*dt)
            print('goTo x=' + str(round(self.x, 3)) + '; y=' + str(round(self.y, 3)) + '; z=' + str(round(self.z, 3)))
            time.sleep(dt)
        self.clear()
        self.publisher_parameters.publish(self.parameters)
        

    def clear(self):
        self.parameters.linear.x = 0.0
        self.parameters.linear.y = 0.0
        self.parameters.linear.z = 0.0
        self.parameters.angular.x = 0.0
        self.parameters.angular.y = 0.0
        self.parameters.angular.z = 0.0
    def timer_callback(self):
        pass
    def listener_callback(self, msg):
        self.get_logger().info('I heard: "%s"' % msg.pose)





def main(args=None):
    print("#######################################################")
    rclpy.init(args=args)
    print("dron test")
    import numpy as np
  
    Data = np.genfromtxt("circle.txt", dtype=float,
                        encoding=None, delimiter=",")
    minimal_publisher = MinimalPublisher()
    # minimal_publisher.goTo(50, 100, 0, 0.1)
    for i in Data:
        print(i[0]/2, i[1]/2, i[2])
        minimal_publisher.goTo(i[0]/2, i[1]/2, 0.0, 0.1)
        minimal_publisher.clear()

    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
