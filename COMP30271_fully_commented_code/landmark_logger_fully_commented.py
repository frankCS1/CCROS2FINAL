
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from datetime import datetime
import csv

class LandmarkLogger(Node):
    def __init__(self):
        super().__init__('landmark_logger')

        # Subscribe to /object_counts topic which receives object detection labels
        # Messages are simple strings like "3 orange, 2 banana"
        # Each message will be passed to the self.listener_callback function
        self.subscription = self.create_subscription(
            String,
            '/object_counts',
            self.listener_callback,
            10)

        # Define the path where the log file will be saved
        self.log_file_path = '/tmp/landmark_log.csv'

        # Open the file in append mode and write the header row (if new)
        with open(self.log_file_path, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(['timestamp', 'detections'])

    def listener_callback(self, msg):
        """
        This function is called whenever a new message arrives on /object_counts.

        It logs:
        - The current timestamp
        - The raw detection string received (e.g., '3 apple, 1 car')

        These logs are saved to a CSV file so that the detection history can be reviewed later.
        This is useful for analysis or audit of the robot's visual environment.
        """
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        detections = msg.data

        # Append the timestamp and detection string to the CSV file
        with open(self.log_file_path, 'a') as f:
            writer = csv.writer(f)
            writer.writerow([current_time, detections])

        # Also print the event to the console/log for live feedback
        self.get_logger().info(f'Logged: {detections} at {current_time}')

def main(args=None):
    # Initialise the ROS 2 client library
    rclpy.init(args=args)

    # Create an instance of the LandmarkLogger node
    node = LandmarkLogger()

    # Spin keeps the node alive and processing callbacks
    rclpy.spin(node)

    # Clean up when exiting
    node.destroy_node()
    rclpy.shutdown()
