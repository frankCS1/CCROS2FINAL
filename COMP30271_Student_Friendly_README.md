
# COMP30271 ROS2 Robot System – Function Overview

This project brings together several key ROS2 nodes that work together to support navigation, detection, and environment awareness. Below is a summary of how the system is structured and how different parts can be run or observed.

---

## 🔧 Environment Setup

From within the ROS2 workspace:

```bash
cd ~/ros2_ws
colcon build --packages-select my_robot_vision_pkg
source install/setup.bash
```

---

## 🧭 Overview of Features

### Mapping (SLAM)
To start building a map, launch:

```bash
ros2 launch my_robot_vision_pkg rtabmap_slam_launch.py
```

In RViz, visualising the `/map`, `/odom`, and TF frames will give a live view of the environment being scanned as the robot moves.

---

### Wall Following
To enable navigation near walls or obstacles:

```bash
ros2 run my_robot_vision_pkg wall_follow_node
```

This will guide the robot forward while adjusting its course if there are objects in front or gaps to the left.

---

### Object Detection
To activate object detection:

```bash
ros2 run my_robot_vision_pkg vision_node
ros2 topic echo /object_counts
```

The system identifies objects and publishes descriptions over a topic. These can then be used by other nodes.

---

### Goal Recognition
Start this by running:

```bash
ros2 run my_robot_vision_pkg goal_node
```

If a goal object is detected in the stream, a command is issued to stop movement, assuming a destination has been reached.

---

### Sign-Based Control
To respond to changes like stop or speed-up signs:

```bash
ros2 run my_robot_vision_pkg traffic_node
ros2 run my_robot_vision_pkg control_node
```

Test changes by publishing simulated input:
```bash
ros2 topic pub /object_counts std_msgs/String "data: 'stop'"
```

---

### Move to Target
Launch the motion controller:

```bash
ros2 run my_robot_vision_pkg nav_node
```

You can use RViz’s 2D Nav Goal tool or let the robot navigate to a preset target using odometry feedback.

---

### Logging What’s Seen
To keep a record of detected objects over time:

```bash
ros2 run my_robot_vision_pkg landmark_logger
```

The log file is saved in `/tmp/landmark_log.csv` and can be opened in a spreadsheet tool.

---

### Viewing Detection Output
The output of object detection is already printed to:

```bash
ros2 topic echo /object_counts
```

Useful for testing responses and logging at the same time.

---

### Observing Motion and Feedback
These are good for checking how the system is responding:

```bash
ros2 topic echo /cmd_vel        # Movement commands
ros2 topic echo /odom           # Position data
```

---

### Direct Control (if needed)
For quick testing without automation:

```bash
ros2 topic pub --rate 5 /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.15}}"
ros2 topic pub --rate 5 /cmd_vel geometry_msgs/msg/Twist "{angular: {z: 0.5}}"
ros2 topic pub /cmd_vel geometry_msgs/msg/Twist "{}"
```

---

This system has been put together in a way that allows easy testing and observation of individual behaviours. The code is structured to show how vision, control, and movement can work together in a simple ROS2 robot setup.
