
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

class WallFollowNode(Node):
    def __init__(self):
        super().__init__('wall_follow_node')

        # Subscribe to /scan topic which contains LIDAR/laser distance data
        # This is used to detect nearby obstacles and walls
        self.subscriber = self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            10)

        # Publisher to /cmd_vel, which controls robot movement
        # We send Twist messages here to make the robot drive or turn
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)

    def scan_callback(self, msg):
        """
        Called every time a new LaserScan message is received.
        LaserScan.ranges is an array of distances (in meters) around the robot.
        Index 0 = front, index 90 = left side (assuming 180-degree LIDAR).

        Logic:
        - If an obstacle is closer than 0.5 meters in front → turn right
        - If there's no wall on the left (distance > 1.0) → turn left to re-align
        - If a wall is beside the robot and the front is clear → move forward
        """
        front = msg.ranges[0]    # Directly ahead
        left = msg.ranges[90]    # Directly to the left

        twist = Twist()  # Create a velocity command

        if front < 0.5:
            # Something directly ahead → stop and turn right
            twist.linear.x = 0.0
            twist.angular.z = -0.5
            self.get_logger().info('Obstacle detected in front. Turning right.')
        elif left > 1.0:
            # No wall on left → turn left to find wall
            twist.linear.x = 0.0
            twist.angular.z = 0.5
            self.get_logger().info('Wall missing on left. Turning left.')
        else:
            # Wall beside robot, path ahead is clear → move forward
            twist.linear.x = 0.15
            twist.angular.z = 0.0
            self.get_logger().info('Wall detected on left. Moving forward.')

        # Send the velocity command to the robot
        self.publisher.publish(twist)

def main(args=None):
    # Initialise the ROS2 system
    rclpy.init(args=args)

    # Create the wall-following node
    node = WallFollowNode()

    # Keep the node running and listening for data
    rclpy.spin(node)

    # Shutdown cleanly after Ctrl+C or exit
    node.destroy_node()
    rclpy.shutdown()
