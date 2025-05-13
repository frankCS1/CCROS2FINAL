
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class TrafficNode(Node):
    def __init__(self):
        super().__init__('traffic_node')

        # Subscribe to object detection results on /object_counts
        # The message type is String, which will contain detected object labels
        # When a new message arrives, self.listener_callback is called
        # Queue size 10 buffers messages if the subscriber is slow to respond
        self.subscription = self.create_subscription(
            String,
            '/object_counts',
            self.listener_callback,
            10)

    def listener_callback(self, msg):
        """
        Called when a new message is received from /object_counts.
        This example node just logs detection results — it can be expanded to trigger specific responses.
        """
        self.get_logger().info(f'TrafficNode received detection: "{msg.data}"')

def main(args=None):
    # Start the ROS2 Python client
    rclpy.init(args=args)

    # Instantiate and spin the node
    node = TrafficNode()
    rclpy.spin(node)

    # Graceful shutdown
    node.destroy_node()
    rclpy.shutdown()
