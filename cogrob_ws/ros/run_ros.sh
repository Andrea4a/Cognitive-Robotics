#! /bin/bash

# Setting Pepper IP
#PEPPER_ADDRESS='10.0.1.230'
#PEPPER_ADDRESS='10.0.1.207'

# Launch roscore in the first terminal
gnome-terminal --tab -- bash -c 'roscore;'
sleep 5

# Launch pepper nodes and pepper tts client in another terminal
gnome-terminal --window -- bash -c 'source devel/setup.bash; roslaunch pepper_nodes pepper_bringup.launch nao_ip:='$PEPPER_ADDRESS'; read'
gnome-terminal --window -- bash -c 'source devel/setup.bash; roslaunch pepper_nodes pepper_tts_client.launch nao_ip:='$PEPPER_ADDRESS'; read'
#sleep 5

# Launch rasa_ros for chatbot in another terminal
gnome-terminal --window -- bash -c 'export PROJECT_WORK_DIR=$(pwd); source devel/setup.bash; roslaunch rasa_ros dialogue.launch; read'
#sleep 5

# Launch engagement person nodes in another terminal
gnome-terminal --window -- bash -c 'source devel/setup.bash; roslaunch engagement_nodes person_engagement.launch; read'
sleep 5

# Launch speech recognition nodes
gnome-terminal --window -- bash -c 'source devel/setup.bash; roslaunch ros_audio_pkg speech_recognition.launch; read'
