# To build:
# docker build --pull --no-cache --tag tello_ros:foxy .

FROM osrf/ros:foxy-desktop

RUN apt-get update
RUN apt-get upgrade -y

RUN apt-get install -y libasio-dev
RUN apt-get install -y python3-pip
RUN yes | pip3 install 'transformations==2018.9.5'
