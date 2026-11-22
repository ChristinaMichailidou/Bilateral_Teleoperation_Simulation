# Bilateral Teleoperation Simulation

ROS 2 Humble simulation integrating the **Franka Research 3 (FR3)** and the **Clearpath Jackal J100 equipped with a Kinova Gen3 Lite** in a shared Gazebo Fortress environment.

The repository provides the ROS 2 package required to launch both robotic systems in the same simulation world.

## 1. Project Overview

The simulation includes:

- Franka Research 3 (FR3), a 7-DoF robotic manipulator.
- Clearpath Jackal J100 with Kinova Gen3 Lite, a 6-DoF manipulator.
- A shared lightweight Gazebo Fortress world.
- ROS 2 controllers for both robotic systems.
- RViz2 visualization.

The simulation provides the foundation for research in bilateral teleoperation, Cartesian pose mapping, and force feedback.

This repository focuses on the shared simulation environment rather than the complete bilateral teleoperation control implementation.

## 2. System Requirements

The project was developed and tested using:

- Ubuntu 22.04 LTS
- ROS 2 Humble
- Gazebo Fortress
- `ros_gz` and `ros2_control`
- Franka ROS 2 packages
- Clearpath ROS 2 packages
- Clearpath Jackal J100 and Kinova Gen3 Lite configuration

**Important:** ROS 2 Humble and the Franka and Clearpath dependencies must be installed before building this repository.

The Franka and Clearpath packages are external dependencies and are not included in this repository.

Additional installation information is available in `docs/installation.md`.

## 3. Repository Structure

```text
Bilateral_Teleoperation_Simulation/
├── README.md
├── .gitignore
├── config/
│   └── robot.simulation.example.yaml
├── docs/
│   └── installation.md
├── patches/
│   └── franka/
│       └── franka_all_changes.patch
├── src/
│   └── dual_robot_viz/
│       ├── dual_robot_viz/
│       │   └── __init__.py
│       ├── launch/
│       │   ├── dual_robot_gazebo.launch.py
│       │   └── dual_robot_viz.launch.py
│       ├── worlds/
│       │   └── empty.sdf
│       ├── resource/
│       ├── package.xml
│       ├── setup.py
│       └── setup.cfg
└── worlds/
    └── empty.sdf
```

## 4. Downloading the Repository

Open a terminal and source ROS 2 Humble:

```bash
source /opt/ros/humble/setup.bash
```

Navigate to the home directory:

```bash
cd ~
```

Clone this repository into the dual-robot workspace:

```bash
git clone https://github.com/ChristinaMichailidou/Bilateral_Teleoperation_Simulation.git dual_robot_ws
```

The repository already contains the `src` directory and the ROS 2 package `dual_robot_viz`.

## 5. Building the Workspace

After installing the required Franka and Clearpath packages, execute:

```bash
source /opt/ros/humble/setup.bash
source ~/franka_ros2_ws/install/setup.bash

cd ~/dual_robot_ws
colcon build --symlink-install
```

After successful compilation, source the workspace:

```bash
source ~/dual_robot_ws/install/setup.bash
```

The package can be checked using:

```bash
ros2 pkg prefix dual_robot_viz
```

## 6. Launching the Dual-Robot Simulation

Open a new terminal.

Source the required environments:

```bash
source /opt/ros/humble/setup.bash
source ~/clearpath/setup.bash
source ~/franka_ros2_ws/install/setup.bash
source ~/dual_robot_ws/install/setup.bash
```

For VMware environments, software rendering may be enabled using:

```bash
export LIBGL_ALWAYS_SOFTWARE=1
```

Launch the simulation:

```bash
ros2 launch dual_robot_viz dual_robot_gazebo.launch.py
```

The launch file starts the Clearpath simulation and spawns the Franka FR3 in the same lightweight Gazebo world.

The Franka is placed at approximately `(1.5, 0.0, 0.0)` metres relative to the Gazebo world origin.

The Franka spawn is delayed to allow the Gazebo simulation to initialize.

## 7. Simulation Architecture

The custom launch file performs the following operations:

1. Starts the Clearpath Gazebo simulation containing the Jackal J100 and Kinova Gen3 Lite.
2. Loads the shared lightweight `empty.sdf` world.
3. Generates the Franka FR3 robot description from its Gazebo Xacro file.
4. Starts the Franka robot state publisher under the `/franka` namespace.
5. Spawns the Franka in the same Gazebo environment.
6. Loads the Franka controllers through its own controller manager.

Both robotic systems share the same simulated world while maintaining independent ROS 2 controller managers.

## 8. Inspecting the Controllers

### Franka FR3

```bash
ros2 control list_controllers \
  -c /franka/controller_manager
```

The Franka configuration includes the joint state broadcaster, gravity compensation example controller, and position controller.

The position controller is initially loaded as inactive in the tested launch configuration.

### Jackal J100 and Kinova Gen3 Lite

```bash
ros2 control list_controllers \
  -c /j100_0000/controller_manager
```

The Kinova system includes a joint trajectory controller, gripper controller, and joint state broadcaster. The mobile platform may also expose its own velocity controller.

Controller states and available interfaces can be inspected using the ROS 2 control command-line tools.

## 9. Kinova Home Configuration

The Kinova Gen3 Lite can be moved to its SRDF-defined home/ready configuration:

```text
[0.0, 0.0, 1.5708, 1.5708, 1.5708, -1.5708]
```

The corresponding arm trajectory action is:

```text
/j100_0000/arm_0_joint_trajectory_controller/follow_joint_trajectory
```

The joint trajectory controller must be active before sending motion goals.

## 10. Simulation Notes

- The Franka uses the `/franka` namespace.
- The Clearpath robot uses the `/j100_0000` namespace.
- The Franka simulation configuration uses `gazebo_effort=true`.
- The Franka gripper is disabled in the shared Gazebo launch configuration.
- The simulation uses a lightweight Gazebo world to reduce computational requirements.
- Robot controllers may require different command interfaces; inspect their states before sending commands.
- Gazebo and RViz serve different purposes: Gazebo simulates the physical environment, while RViz visualizes robot states and ROS 2 data.

## 11. Stopping the Simulation

Return to the terminal in which the simulation was launched and press:

```text
Ctrl+C
```

Stop the existing simulation before launching another Gazebo environment.

## 12. Documentation and Reproducibility

Additional setup materials are provided in:

- `docs/installation.md`
- `config/robot.simulation.example.yaml`
- `patches/franka/franka_all_changes.patch`

The dual-robot simulation has been tested on the development system. A complete clean-machine installation and reproducibility check is planned.

This repository does not include the complete Franka and Clearpath source distributions or the full bilateral teleoperation implementation.
