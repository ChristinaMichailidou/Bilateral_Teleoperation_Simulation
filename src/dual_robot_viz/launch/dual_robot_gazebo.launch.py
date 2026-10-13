import os
import xacro

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import (
    IncludeLaunchDescription,
    RegisterEventHandler,
    TimerAction,
    SetEnvironmentVariable,
)
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node


def generate_launch_description():

    # -----------------------------
    # Clearpath Gazebo simulation
    # -----------------------------
    clearpath_gz_share = get_package_share_directory('clearpath_gz')

    clearpath_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                clearpath_gz_share,
                'launch',
                'simulation.launch.py'
            )
        ),
        launch_arguments={
            'world': os.path.expanduser(
                '~/dual_robot_ws/worlds/empty'
             )
        }.items()
    )

    # -----------------------------
    # Franka robot_description
    # -----------------------------
    franka_gazebo_share = get_package_share_directory(
        'franka_gazebo_bringup'
    )

    franka_xacro_file = os.path.join(
        franka_gazebo_share,
        'urdf',
        'franka_arm.gazebo.xacro'
    )

    robot_description_config = xacro.process_file(
        franka_xacro_file,
        mappings={
            'robot_type': 'fr3',
            'hand': 'false',
            'gazebo': 'true',
            'ee_id': 'franka_hand',
            'gazebo_effort': 'false',
            'robot_namespace': 'franka',
        }
    )

    robot_description = {
        'robot_description': robot_description_config.toxml()
    }

    franka_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        namespace='franka',
        name='robot_state_publisher',
        parameters=[robot_description],
        output='screen'
    )

    # -----------------------------
    # Spawn Franka into SAME Gazebo
    # -----------------------------
    franka_spawn = Node(
        package='ros_gz_sim',
        executable='create',
        name='spawn_franka',
        arguments=[
            '-topic', '/franka/robot_description',
            '-name', 'franka_fr3',
            '-x', '1.5',
            '-y', '0.0',
            '-z', '0.0'
        ],
        output='screen'
    )

    # Clearpath/Gazebo needs some time to start first
    delayed_franka_spawn = TimerAction(
        period=20.0,
        actions=[franka_spawn]
    )

    # -----------------------------
    # Franka controllers
    # -----------------------------
    franka_controllers = Node(
        package='controller_manager',
        executable='spawner',
        arguments=[
            'joint_state_broadcaster',
            'gravity_compensation_example_controller',
            '--controller-manager',
            '/franka/controller_manager',
            '--controller-manager-timeout', '30',
        ],
        parameters=[
            os.path.join(
                franka_gazebo_share,
                'config',
                'franka_gazebo_controllers.yaml'
            )
        ],
        output='screen'
    )

    start_controllers_after_spawn = RegisterEventHandler(
        OnProcessExit(
            target_action=franka_spawn,
            on_exit=[franka_controllers]
        )
    )

    # Add Franka resources without replacing existing Gazebo paths
    franka_description_parent = os.path.dirname(
        get_package_share_directory('franka_description')
    )

    existing_resource_path = os.environ.get('GZ_SIM_RESOURCE_PATH', '')

    combined_resource_path = os.pathsep.join(
        p for p in [
            existing_resource_path,
            franka_description_parent,
            franka_gazebo_share
        ] if p
    )

    gz_resource_path = SetEnvironmentVariable(
        'GZ_SIM_RESOURCE_PATH',
        combined_resource_path
    )

    return LaunchDescription([
        gz_resource_path,
        clearpath_sim,
        franka_state_publisher,
        delayed_franka_spawn,
        start_controllers_after_spawn,
    ])
