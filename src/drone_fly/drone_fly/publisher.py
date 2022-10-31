import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(Twist, '/drone1/cmd_vel', 10)
        timer_period = 2  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        # self.i = 0
        self.flag = True

    def timer_callback(self):
        twist = Twist()
        if self.flag:
            twist.linear.x = 0.1
            self.flag = False
        else:
            twist.linear.x = 0.0

        self.publisher_.publish(twist)
        #self.get_logger().info('Publishing: "%s"' % msg.data)
        #self.i += 1


def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher()

    rclpy.spin(minimal_publisher)
    print("done")

    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
