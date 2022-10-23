rocker --network host --privileged --nvidia --x11 --user --name drone_ws \
  	--env="USER" \
	--volume /dev/shm \
	--volume $HOME/Studia/ARL-Retinger/drone_ws:$HOME/drone_ws \
	--volume /opt/pycharm-community-2022.1.1:/opt/pycharm \
	-- tello_ros:foxy
