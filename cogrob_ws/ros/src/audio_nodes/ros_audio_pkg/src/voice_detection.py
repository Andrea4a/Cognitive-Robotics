#!/usr/bin/python3
import rospy
from std_msgs.msg import Int16MultiArray, Bool
import numpy as np

import time
import speech_recognition as sr

pub = rospy.Publisher('mic_data', Int16MultiArray, queue_size=10)

rospy.init_node('voice_detection_node', anonymous=False)


# setting the engagement of the person initially to False
is_person_engaged = False

def is_pepper_speaking_callback(is_speaking):
    """
    Funzione di callback che viene chiamata quando pepper sta parlando, 
    disattiva il microfono, cosi che non possa asclatre la sua voce
    """

    global stop_listening
    global is_person_engaged

    # if is_person_engaged:
    # if person is engaged it deactivate the microphone
    if is_speaking.data:
        print('Pepper is speaking, stop listening...')
    
        # stopping background listening
        stop_listening()
        
    else:
        print('Pepper has done speaking, start listening...')
        # starting again background listening
        stop_listening = r.listen_in_background(m, callback)
        
def detection_callback(is_person_detected):
    """
    Funzione di callback, viene chiamata quando viene rilevata una paersona
    Se la persona viene rilevata inizia a parlare, altrimenti disattiva il microfono
    """
    global stop_listening
    global is_person_engaged

    if is_person_detected.data:
        is_person_engaged = True
        print('Persona rilevata, in ascolto...')
        try:
            # starting again background listening
            stop_listening = r.listen_in_background(m, callback)
        except:
            pass
    else:
        is_person_engaged = False
        print('Persona non rilevata, ascolto disattivato...')
        try:
            # stopping background listening
            stop_listening()
        except:
            pass

# this is called from the background thread
def callback(recognizer, audio):
    data = np.frombuffer(audio.get_raw_data(), dtype=np.int16)
    data_to_send = Int16MultiArray()
    data_to_send.data = data
    pub.publish(data_to_send)


pub = rospy.Publisher('mic_data', Int16MultiArray, queue_size=10)

rospy.init_node('voice_detection_node', anonymous=False)


# setting the engagement of the person initially to False
is_person_engaged = False

rospy.Subscriber('is_pepper_speaking', Bool, is_pepper_speaking_callback)
#rospy.Subscriber('detection', Detection2DArray, detection_callback)


# Initialize a Recognizer
r = sr.Recognizer()
r.dynamic_energy_threshold = False 
for i, mic_name in enumerate(sr.Microphone.list_microphone_names()):
    print(f"{i}: {mic_name}")
m = sr.Microphone(device_index=None,
                    sample_rate=16000,
                    chunk_size=1024)

# Calibration within the environment
# we only need to calibrate once, before we start listening
print("Calibrating...")
with m as source:
    r.adjust_for_ambient_noise(source,duration=3)  
    #r.energy_threshold = 150 #Modify here to set threshold. Reference: https://github.com/Uberi/speech_recognition/blob/1b737c5ceb3da6ad59ac573c1c3afe9da45c23bc/speech_recognition/__init__.py#L332

print("Calibration finished")

# start listening in the background
# `stop_listening` is now a function that, when called, stops background listening
stop_listening = r.listen_in_background(m, callback)

rospy.spin()