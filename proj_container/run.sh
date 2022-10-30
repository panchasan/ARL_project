rocker --network host --privileged --nvidia --x11 --user --name drone_ws \
  	--env="USER" \
	--volume /dev/shm \
	--volume $HOME/ARL/ARL_project:$HOME/drone_ws \
	-- tello_ros:foxy
