# ARL project


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
cd drone_ws
sudo apt-get update
rosdep update
vcs import src < drone.repos
rosdep install --from-paths src --ignore-src -yr
colcon build --symlink-install --cmake-args -DCMAKE_BUILD_TYPE=Debug -DCMAKE_EXPORT_COMPILE_COMMANDS=1
source install/setup.bash
```
Running the demo:
```
source install/setup.bash
ros2 launch tello_gazebo simple
```
## Configuring the container
Every time the container is started with `run.sh` script, it should be followed by `setup.sh` script. The terminal where the script was run will not have full functionality. Enter the container from the other terminal with `enter.sh` script. It will look as follows:

```
(foxy) user@machine:~/drone_ws (master #%)$
```
