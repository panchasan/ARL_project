sudo apt-get update

sudo apt-get -y install libasio-dev

rosdep update
rosdep install --from-paths ${HOME}/drone_ws/src --ignore-src -yr
echo "source ${HOME}/drone_ws/proj_container/git-prompt.sh" >> ${HOME}/.bashrc
echo "source ${HOME}/drone_ws/proj_container/env-vars" >> ${HOME}/.bashrc
echo "source ${HOME}/drone_ws/install/setup.bash" >> ${HOME}/.bashrc
sudo usermod -G dialout -a ${USER}
sudo usermod -G root -a ${USER}
source ${HOME}/.bashrc
pip install asyncio
pip install google
pip install --upgrade google-api-python-client
pip install protobuf==3.20.3

