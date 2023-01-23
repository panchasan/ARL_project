# ARL project
## Purpose
Welcome to our project on Autonomous Flying Robots. The goal of this project was to develop software using the Robot Operating System (ROS) and the librosa library that processes music file, the trajectory is generated based on a music file, and then executes that trajectory by the drone in sync with the music. The simulation was initially conducted in the Gazebo environment, and later on a real Tello drone. 
Packge uses g2rr script that was shared to us and script for Optitrack. 


### Input

| Name         | Type                  | Description  |
| ------------ | --------------------- | ------------ |
| `optitrack_topic` | nav_msgs/Pose | Topic that gives us feedback about actual postion of a drone |

### Output

| Name         | Type                  | Description  |
| ------------ | --------------------- | ------------ |
| `/cmd_vel` | geometry_msgs/Twist  | Topic where orders are send |


### Dependencies
- [rocker](https://github.com/osrf/rocker)
  - We use `rocker` to enable GUI applications such as `rviz` and `rqt` on Docker Containers.
  - Refer to [here](http://wiki.ros.org/docker/Tutorials/GUI) for more details.

## Installation with Docker

Download repository
```
git clone https://github.com/panchasan/ARL_project.git
```

Build docker image from delivered Dockerfile

```
cd ARL_project/
docker build --pull --no-cache --tag tello_ros:foxy .
```

Run container with delivered script `run.sh`
```
cd drone_ws
./proj_container/run.sh
```

Install dependencies & build workspace
```
cd dron_ws
sudo apt-get update
rosdep update
vcs import src < drone.repos
rosdep install --from-paths src --ignore-src -yr
colcon build --symlink-install --cmake-args -DCMAKE_BUILD_TYPE=Debug -DCMAKE_EXPORT_COMPILE_COMMANDS=1
source install/setup.bash
```

## Configuring the container
Every time the container is started with `run.sh` script, it should be followed by `setup.sh` script. The terminal where the script was run will not have full functionality. Enter the container from the other terminal with `enter.sh` script. It will look as follows:

```
(foxy) user@machine:~/drone_ws (master #%)$
```

## Run the simulation

```
po kolei uruchomienie 
```


