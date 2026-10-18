# Mavi Gölge ROS 2 Eğitimi — çalışma ortamı
# Temel imaj: ROS 2 Jazzy "desktop" (turtlesim, rqt, rviz2 dahil).
FROM osrf/ros:jazzy-desktop

ARG DEBIAN_FRONTEND=noninteractive

# Geliştirme araçları: colcon, rosdep, vcstool (ros-dev-tools) ve pytest.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ros-dev-tools \
        python3-pytest \
        git \
        nano \
    && rm -rf /var/lib/apt/lists/*

# Her etkileşimli terminal ROS ortamıyla açılsın.
RUN echo "source /opt/ros/jazzy/setup.bash" >> /etc/bash.bashrc
