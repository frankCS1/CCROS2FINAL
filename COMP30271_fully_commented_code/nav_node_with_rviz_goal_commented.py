
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, PoseStamped
from nav_msgs.msg import Odometry
import math

class NavNode(Node):
    def __init__(self):
        super().__init__('nav_node')

        # Publisher to control robot movement via velocity commands
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)

        # Subscriber to odometry topic to track robot's current position
        self.subscription = self.create_subscription(
            Odometry,
            '/odom',
            self.odom_callback,
            10)
        self.subscription  # Avoid unused variable warning

        # Default hardcoded goal (can be overridden by RViz goal input)
        self.goal_x = 2.0
        self.goal_y = 2.0
        self.goal_received = False

        # Subscriber to goal pose published from RViz's "2D Nav Goal"
        self.goal_sub = self.create_subscription(
            PoseStamped,
            '/goal_pose',
            self.goal_callback,
            10
        )

        # Variables to hold current robot position
        self.current_x = 0.0
        self.current_y = 0.0

    def goal_callback(self, msg):
        """
        Callback function for RViz 2D Nav Goal input.
        Updates the target coordinates with the values from the PoseStamped message.
        """
        self.goal_x = msg.pose.position.x
        self.goal_y = msg.pose.position.y
        self.goal_received = True
        self.get_logger().info(f"New goal received from RViz: x={self.goal_x}, y={self.goal_y}")

    def odom_callback(self, msg):
        """
        Callback function that is triggered whenever new odometry data is received.
        It calculates the direction and distance to the goal and publishes velocity commands accordingly.
        """
        self.current_x = msg.pose.pose.position.x
        self.current_y = msg.pose.pose.position.y

        # Calculate vector to goal
        dx = self.goal_x - self.current_x
        dy = self.goal_y - self.current_y
        distance = math.hypot(dx, dy)

        # Create a Twist message to send to /cmd_vel
        twist = Twist()

        if distance > 0.1:
            # Calculate angle to goal and apply simple proportional motion
            angle_to_goal = math.atan2(dy, dx)
            twist.linear.x = 0.15  # Move forward
            twist.angular.z = angle_to_goal  # Face toward goal
        else:
            # Stop the robot if goal is reached
            twist.linear.x = 0.0
            twist.angular.z = 0.0

        # Publish velocity command
        self.publisher_.publish(twist)

def main(args=None):
    rclpy.init(args=args)
    node = NavNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
