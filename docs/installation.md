# Dual Robot Gazebo Simulation — Installation Guide

## 1. System Requirements

This project was developed and tested with the following environment:

| Component | Version |
|---|---|
| Operating System | Ubuntu 22.04 LTS |
| ROS 2 | Humble Hawksbill |
| Gazebo | Fortress (Ignition Gazebo 6) |
| Clearpath Gazebo | 1.3.3 |
| Robot 1 | Franka FR3 — 7 DoF |
| Robot 2 | Kinova Gen3 Lite — 6 DoF |
| Mobile Platform | Clearpath Jackal J100 |

The goal is to simulate the Franka FR3 and the Jackal-mounted Kinova Gen3 Lite in a shared Gazebo environment for bilateral teleoperation research.

## 2. External Repositories

### Franka ROS 2

Repository: https://github.com/frankarobotics/franka_ros2

Tested commit:

`3b50164eabbe2d461baca007bbbbe03c024387bd`

The project uses a locally modified Franka Gazebo configuration.

Changes are saved in:

`patches/franka/franka_all_changes.patch`

The patch includes experimental controller settings and namespace support. It must be reviewed before applying it to an existing Franka installation.

### Clearpath Robot Simulation

Repository: https://github.com/laloutsos/Custom_Clearpath_Robot

Tested commit:

`48edacc523f2e0d58682b6c3c0f858178a461f37`

Used for the Clearpath Jackal J100 with Kinova Gen3 Lite simulation.

### Kinova ROS 2 Kortex

Repository: https://github.com/Kinovarobotics/ros2_kortex

Tested commit:

`116d87ae595c791ba7ae32201b88693a3ba02324`

This repository was checked and had no uncommitted local modifications.

The version differs from files tracked inside the Laloutsos repository. This must be considered when reproducing the installation.

## 3. Existing Installation Checks

Before modifying any packages on the laboratory computer, verify that ROS 2 and the required packages are available.

```bash
echo $ROS_DISTRO
lsb_release -ds
ign gazebo --versions

ros2 pkg prefix franka_gazebo_bringup
ros2 pkg prefix clearpath_gz
ros2 pkg prefix ros_gz_sim
```

Check the currently installed source repositories before applying any patch or switching commits.

Do not overwrite an existing working laboratory installation without backing up its changes.

## 4. Dual Robot Workspace

Clone the private repository using an account with access:

```bash
cd ~

git clone \
  https://github.com/ChristinaMichailidou/Bilateral_Teleoperation_Simulation.git \
  dual_robot_ws
```

The workspace contains:

- `dual_robot_viz`: Shared Gazebo and RViz launch files
- `worlds/empty.sdf`: Installed inside the ROS 2 package
- `patches/franka/`: Franka simulation modifications
- `config/`: Clearpath simulation configuration template
- `docs/`: Installation and configuration documentation

## 5. Franka Gazebo Configuration

The shared simulation currently uses:

```python
'robot_type': 'fr3',
'hand': 'false',
'gazebo': 'true',
'gazebo_effort': 'false',
'robot_namespace': 'franka',
```

The `robot_namespace` support was added locally to the Franka Gazebo Xacro.

Before using the patch:

1. Check the Franka repository commit.
2. Check for existing local changes.
3. Review the patch contents.
4. Test compatibility without modifying files.

Example compatibility check:

```bash
cd ~/franka_ros2_ws/src/franka_ros2

git status --short
git rev-parse HEAD

git apply --check \
  ~/dual_robot_ws/patches/franka/franka_all_changes.patch
```

Only apply the necessary modifications after confirming compatibility and preserving any existing laboratory configuration.

After source changes, rebuild the affected Franka packages and source the updated workspace.

## 6. Clearpath Configuration

The working development configuration is located at:

`~/clearpath/robot.yaml`

It configures:

- Jackal J100
- Kinova Gen3 Lite
- Kinova 2F Lite gripper
- MoveIt support
- Additional sensors and mounts

The repository contains a simulation template.

Before using the template, review hardware identifiers, IP addresses, workspace paths and dependencies.

The working original configuration must not be overwritten without backup. Documentation-only IP addresses must not be used for physical hardware.

## 7. Build the Dual Robot Workspace

After the Franka and Clearpath dependencies are correctly installed:

```bash
source /opt/ros/humble/setup.bash
source ~/franka_ros2_ws/install/setup.bash

cd ~/dual_robot_ws
colcon build --symlink-install

source install/setup.bash
```

Other dependency workspaces must be sourced if their required packages are not available from the existing ROS environment.

## 8. Launch the Simulation

```bash
ros2 launch dual_robot_viz dual_robot_gazebo.launch.py
```

Expected result:

- Gazebo starts using the empty world.
- Clearpath Jackal with Kinova Gen3 Lite is spawned.
- Franka FR3 is spawned in the same world.
- Franka uses the `/franka` namespace.
- ROS 2 controllers are available.

## 9. Test Franka Controllers

Check available controllers:

```bash
ros2 control list_controllers \
  -c /franka/controller_manager
```

Check hardware interfaces:

```bash
ros2 control list_hardware_interfaces \
  -c /franka/controller_manager
```

For a simulation-only movement test, activate the example position controller:

```bash
ros2 run controller_manager spawner \
  joint_position_example_controller \
  -c /franka/controller_manager
```

Verify that the controller becomes active and that the joint positions change.

This test is intended only to validate Gazebo movement, not bilateral teleoperation.

## 10. Current Status

- Shared Gazebo environment: working
- Empty world: working
- Portable world path: working
- Franka position controller activation: confirmed
- Cartesian 6D mapping: not yet implemented
- Bilateral force feedback: not yet implemented
- Laboratory deployment: not yet tested

## 11. Remaining Installation Verification

The following details must still be verified on the laboratory computer:

- Exact Gazebo and ros2_control package versions
- Presence and compatibility of Franka and Kinova dependencies
- Clearpath configuration compatibility
- Source/build instructions for any missing dependencies
- Necessary subset of Franka patches
- Functionality of both robot controllers after installation

This document records the tested development configuration. It is not yet a fully validated installation procedure for a clean computer.
