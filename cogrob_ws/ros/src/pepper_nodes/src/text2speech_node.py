#!/usr/bin/python3
from utils import Session
from pepper_nodes.srv import Text2Speech
from optparse import OptionParser
import rospy

'''
This class implements a ROS node able to call the Animated Speech service of the robot
'''
class Text2SpeechNode:
    
    '''
    The constructor creates a session to Pepper and initializes the Animated Speech service
    '''
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.session = Session(ip, port)
        # Usa ALAnimatedSpeech invece di ALTextToSpeech
        self.animated_speech = self.session.get_service("ALAnimatedSpeech")
        self.tts = self.session.get_service("ALTextToSpeech")
        self.tts.setLanguage("English")
    '''
    Receives a Text2Speech message and calls the ALAnimatedSpeech service.
    The robot will play the text of the message with random gestures
    '''
    def say(self, msg):
        try:
            # Configurazione per abilitare i gesti casuali
            config = {"bodyLanguageMode": "contextual"}  # Altri valori: "random" o "disabled"
            self.animated_speech.say(msg.speech, config)
        except Exception as e:
            rospy.logerr(f"Error during speech: {e}")
            self.session.reconnect()
            self.animated_speech = self.session.get_service("ALAnimatedSpeech")
            self.animated_speech.say(msg.speech, config)
        return "ACK"
    
    '''
    Starts the node and creates the tts service
    '''
    def start(self):
        rospy.init_node("text2speech_node")
        rospy.Service('tts', Text2Speech, self.say)

        rospy.spin()

if __name__ == "__main__":
    import time
    time.sleep(3)
    parser = OptionParser()
    parser.add_option("--ip", dest="ip", default="10.0.1.207")
    parser.add_option("--port", dest="port", default=9559)
    (options, args) = parser.parse_args()

    try:
        ttsnode = Text2SpeechNode(options.ip, int(options.port))
        ttsnode.start()
    except rospy.ROSInterruptException:
        pass
