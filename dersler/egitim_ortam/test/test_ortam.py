"""Yer tutucu testler: ROS 2 ortamının CI içinde kullanılabilir olduğunu doğrular."""

import os
import shutil
import subprocess


def test_ros_dagitimi_jazzy():
    assert os.environ.get('ROS_DISTRO') == 'jazzy'


def test_rclpy_ice_aktarilabiliyor():
    import rclpy  # noqa: F401


def test_turtlesim_calistirilabilirleri_var():
    assert shutil.which('ros2') is not None
    cikti = subprocess.run(
        ['ros2', 'pkg', 'executables', 'turtlesim'],
        capture_output=True, text=True, timeout=60, check=True,
    ).stdout
    assert 'turtlesim_node' in cikti
    assert 'turtle_teleop_key' in cikti
