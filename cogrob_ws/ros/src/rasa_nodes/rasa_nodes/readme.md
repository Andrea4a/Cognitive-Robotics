# How to run

1. In rasa rasa_ros package
2. cd scripts
	- change in ```rasa_action.sh``` and ```rasa_server.sh``` the ```<PATH TO>``` string with your corrent path that point to rasa_ws folder
3. By rasa_ws build the workspace: ```catkin build```
4. ```source devel/setup.bash```
5. Run rasa server & actions and ros nodes: ```roslaunch rasa_ros dialogue.launch ```
6. Wait for a minute (more or less)
7. Start to chat using CLI
