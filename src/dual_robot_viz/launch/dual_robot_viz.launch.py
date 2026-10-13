from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():

    j100_tf_bridge = Node(
        package='topic_tools',
        executable='relay',
        name='j100_tf_relay',
        arguments=['/j100_0000/tf', '/tf'],
        output='screen'
    )

    j100_tf_static_bridge = Node(
        package='topic_tools',
        executable='relay',
        name='j100_tf_static_relay',
        arguments=['/j100_0000/tf_static', '/tf_static'],
        output='screen'
    )

    world_to_franka = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='world_to_franka',
        arguments=[
            '--x', '0.0',
            '--y', '0.0',
            '--z', '0.0',
            '--roll', '0.0',
            '--pitch', '0.0',
            '--yaw', '0.0',
            '--frame-id', 'world',
            '--child-frame-id', 'base'
        ],
        output='screen'
    )

    world_to_j100 = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='world_to_j100',
        arguments=[
            '--x', '1.5',
            '--y', '0.0',
            '--z', '0.0',
            '--roll', '0.0',
            '--pitch', '0.0',
            '--yaw', '3.14159',
            '--frame-id', 'world',
            '--child-frame-id', 'base_link'
        ],
        output='screen'
    )

    rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='dual_robot_rviz',
        output='screen'
    )

    return LaunchDescription([
        j100_tf_bridge,
        j100_tf_static_bridge,
        world_to_franka,
        world_to_j100,
        rviz,
    ])
