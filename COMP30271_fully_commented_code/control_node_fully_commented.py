
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Twist

class ControlNode(Node):
    def __init__(self):
        super().__init__('control_node')

        # Subscribe to /object_counts to detect traffic signs like STOP, SLOW, SPEED
        self.subscription = self.create_subscription(
            String,
            '/object_counts',
            self.listener_callback,
            10)

        # Publisher to /cmd_vel to send motion commands
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)

    def listener_callback(self, msg):
        """
        This callback reacts to detected signs by changing robot behaviour:
        - If the message contains 'stop', the robot stops completely.
        - If it contains 'slow', the robot moves slowly.
        - If it contains 'speed', the robot moves faster.
        This provides a way for visual input (e.g., signs) to control motion.

        Why Twist?
        - Twist is used to send movement commands to the robot.
        - linear.x = forward speed, angular.z = turn rate.
        - Publishing to /cmd_vel makes the robot execute the movement.
        """
        twist = Twist()

        if 'stop' in msg.data.lower():
            twist.linear.x = 0.0
            twist.angular.z = 0.0
            self.get_logger().info('Traffic sign detected: STOP. Robot stopping.')

        elif 'slow' in msg.data.lower():
            twist.linear.x = 0.1
            twist.angular.z = 0.0
            self.get_logger().info('Traffic sign detected: SLOW. Reducing speed.')

        elif 'speed' in msg.data.lower():
            twist.linear.x = 0.3
            twist.angular.z = 0.0
            self.get_logger().info('Traffic sign detected: SPEED. Increasing speed.')

        else:
            # No action taken for unknown labels
            twist.linear.x = 0.15
            twist.angular.z = 0.0
            self.get_logger().info('Default motion. No traffic change detected.')

        # Send velocity command to the robot
        self.publisher.publish(twist)

def main(args=None):
    # Start the ROS2 system
    rclpy.init(args=args)

    # Create the node
    node = ControlNode()

    # Keep the node alive and listening
    rclpy.spin(node)

    # Clean shutdown when stopped
    node.destroy_node()
    rclpy.shutdown()
