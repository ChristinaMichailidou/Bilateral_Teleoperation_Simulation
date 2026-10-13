# Dual Robot Gazebo Simulation

ROS 2 Humble simulation containing the Franka FR3 and Kinova Gen3 Lite in a shared Gazebo environment.

## 1. Project Overview

This project combines:

- Franka FR3 simulation using `franka_ros2`.
- Clearpath Jackal J100 with Kinova Gen3 Lite.
- A shared Gazebo Fortress world.
- ROS 2 controllers for robot motion.
- RViz visualization.

The long-term goal is to develop a bilateral teleoperation system with Cartesian pose mapping and force feedback.

## 2. Architecture

The Clearpath simulation starts Gazebo and spawns the Jackal/Kinova system.

A custom launch file processes the Franka Xacro, publishes its robot description, and spawns the Franka FR3 in the same Gazebo world.

The Franka uses `gz_ros2_control/GazeboSimSystem` in the currently tested configuration (`gazebo_effort=false`).

## 3. Requirements

- Ubuntu and ROS 2 Humble
- Gazebo Fortress
- `ros_gz` / `ros2_control`
- Franka ROS 2 packages
- Clearpath Gazebo simulation packages
- Jackal J100 and Kinova Gen3 Lite configuration

**Installation details and exact dependency versions:** To be documented from the working machine.

## 4. Workspace Setup

After installing and building the dependency workspaces, build the dual robot workspace:

```bash
cd ~/dual_robot_ws
colcon build --symlink-install
```

## 5. Launch the Simulation

In a new terminal:

```bash
source /opt/ros/humble/setup.bash
source ~/franka_ros2_ws/install/setup.bash
source ~/dual_robot_ws/install/setup.bash

ros2 launch dual_robot_viz dual_robot_gazebo.launch.py
```

## 6. Test Franka Movement

List the controllers:

```bash
ros2 control list_controllers -c /franka/controller_manager
```

Activate the example position controller:

```bash
ros2 run controller_manager spawner \
  joint_position_example_controller \
  -c /franka/controller_manager
```

Verify its status:

```bash
ros2 control list_controllers -c /franka/controller_manager
```

This controller is used for simulation testing, not the final teleoperation controller.

## 7. Current Status

- Both robot systems load into a shared Gazebo simulation.
- A custom empty world replaces the warehouse environment.
- Franka position and velocity command interfaces are available.
- Franka joint position example controller has been activated successfully.
- Cartesian mapping and bilateral force feedback are not yet implemented.

## 8. Next Steps

- Verify joint movement from ROS 2 state feedback.
- Implement Cartesian 6D pose mapping.
- Connect Franka EE motion to Kinova EE tracking.
- Develop force estimation and bilateral feedback control.
