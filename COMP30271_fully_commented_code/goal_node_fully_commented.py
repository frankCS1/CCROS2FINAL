
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Twist

class GoalNode(Node):
    def __init__(self):
        super().__init__('goal_node')

        # Subscribe to the topic where detected object names are published.
        # This allows the robot to listen for specific keywords like 'goal'.
        self.subscriber = self.create_subscription(
            String,
            '/object_counts',
            self.listener_callback,
            10)

        # Publisher to the /cmd_vel topic, which is used to control robot motion.
        # The Twist message contains linear and angular velocity settings.
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)

    def listener_callback(self, msg):
        """
        This function is called whenever a message is received on the /object_counts topic.
        It checks whether the string 'goal' appears in the message data.
        If 'goal' is detected, it publishes a Twist message with zero velocity,
        effectively stopping the robot.

        Why use Twist:
        - Twist is the standard message type for controlling robot motion in ROS2.
        - It contains two parts: linear velocity (e.g., forward movement)
          and angular velocity (e.g., turning left/right).
        - Setting both linear.x and angular.z to zero commands the robot to stop completely.
        """
        if 'goal' in msg.data:
            twist = Twist()
            twist.linear.x = 0.0    # Stop forward movement
            twist.angular.z = 0.0   # Stop any rotation
            self.publisher.publish(twist)
            self.get_logger().info('Goal detected! Robot stopping.')

def main(args=None):
    # Initialize ROS2 Python interface
    rclpy.init(args=args)

    # Create and spin the node until manually shut down
    node = GoalNode()
    rclpy.spin(node)

    # Clean shutdown of the node
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
