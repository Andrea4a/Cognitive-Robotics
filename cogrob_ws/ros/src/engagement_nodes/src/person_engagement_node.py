#!/usr/bin/env python3
from optparse import OptionParser


import rospy
from std_msgs.msg import String, Bool, Float32MultiArray
import random
from vision_msgs.msg import Detection2DArray

import qi
import sys

'''
This class creates a qi session using the ip and port parameters provided as input to costructor
'''
class Session:
    '''
    The costructor creates a qi session object. It then uses the ip and port parameters to connect the object to Pepper OS
    '''
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self._session = qi.Session()
        self._connect()
    
    '''
    This method uses the session object to connect to Pepper OS. If an exception occurs, the application is killed.
    '''
    def _connect(self):
        try:
            self.session.connect("tcp://" + self.ip + ":" + str(self.port))
        except RuntimeError:
            print("Can't connect to Naoqi at ip \"" + self.ip + "\" on port " + str(self.port) + ".\n "
                                                                                                 "Please check your script arguments. Run with -h option for help.")
            sys.exit(1)

    '''
    This method reconnect the session object to Pepper OS
    @return: Returns the session object
    '''
    def reconnect(self):
        self._connect()
        return self.session
    
    '''
    Getter for the session object
    '''
    @property
    def session(self):
        return self._session
    
    '''
    This method returns the NaoQi service given as parameter.
    @param service_name: The name of the NaoQi service in form of string
    @return: Returns the service object
    '''
    def get_service(self, service_name: str):
        return self.session.service(service_name)


# boolean variable that indicates if a person has been engaged
is_person_engaged = False

# list of sentences to say when engagement starts
presence_sentences = ["Hey, how can I help you?",
                      "Do you need help?",
                      "Hey, if I can help you ask without hesitation",
                      "Hi, is there anything I can do to make myself useful",
                      "Hi, my name is Pepper, if you're searching for someone just ask",
                      "Hey, I'm Pepper, if you're searching for someone just ask"]

# list of sentences to say when engagement finishes
absence_sentences = ["Goodbye",
                     "Have a nice day!",
                     "Bye bye",
                     "See you next time"]


"""
Callback for the "detection" topic, if a person gets detected, it waits time_to_wait seconds for the person
to talk, if the person doesn't talk, it publishes on "bot_answer" topic a random sentence in presence_sentences and sets
the is_person_engaged to True.
If the person is engaged but no person is detected, it publishes on "bot_answer" topic a random sentence in 
absence_sentences, and sets the is_person_engaged to False.
"""
def detection_callback(is_person_detected):
    global is_person_engaged

    if is_person_detected.data:
        time_to_wait = 1
        try:
            # waits for time_to_wait seconds that person speaks
            txt = rospy.wait_for_message("voice_txt", String, time_to_wait)
        except Exception:
            txt = None

        is_person_engaged = True

        # if txt is None it means the person didn't speak
        if txt is None:
            rospy.loginfo("No interaction")
            data_to_send = String()
            data_to_send.data = random.choice(presence_sentences)
            pub_answer.publish(data_to_send)
        else:
            rospy.loginfo("Person interacted!")
    else:
        # if a person was engaged it sets the is_person_engaged to False and
        # publishes on topic a random sentences meaning the engagement is finished
        if is_person_engaged:
            is_person_engaged = False

            # publishing randomly one of the absence_sentences
            data_to_send = String()
            data_to_send.data = random.choice(absence_sentences)
            pub_answer.publish(data_to_send)

            # resetting head position to default
            tracker_service.unregisterAllTargets()
            tracker_service.stopTracker()

            head_reset_yaw.publish(default_yaw_position)
            head_reset_pitch.publish(default_pitch_position)

            targetName = "Face"
            faceWidth = 0.1
            tracker_service.registerTarget(targetName, faceWidth)
            tracker_service.track(targetName)


# defining default position for the head, they are useful when the engagement ends
# in order to reset the head position of Pepper
velocity = 0.15

default_yaw_position = Float32MultiArray()
default_yaw_position.data = [0.0, velocity]

default_pitch_position = Float32MultiArray()
default_pitch_position.data = [-0.1, velocity]


if __name__ == "__main__":
    try:
        parser = OptionParser()
        parser.add_option("--ip", dest="ip", default="10.0.1.207")
        parser.add_option("--port", dest="port", default=9559)
        (options, args) = parser.parse_args()

        # initializing node and all the topic it will use
        rospy.init_node("person_engagement_node")

        pub_answer = rospy.Publisher("bot_answer", String, queue_size=10)
        head_reset_yaw = rospy.Publisher("/head_rotation/yaw", Float32MultiArray, queue_size=10)
        head_reset_pitch = rospy.Publisher("/head_rotation/pitch", Float32MultiArray, queue_size=10)
        sub_det = rospy.Subscriber("detection", Detection2DArray, detection_callback)

        # getting session
        session = Session(options.ip, int(options.port))
        tracker_service = session.get_service("ALTracker")

        rospy.spin()
    except rospy.ROSInterruptException:
        pass